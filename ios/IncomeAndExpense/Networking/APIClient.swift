import Foundation

enum AppError: LocalizedError {
    case invalidURL
    case invalidResponse
    case httpError(statusCode: Int, body: Data)
    case decodingFailed(underlying: Error)

    var errorDescription: String? {
        switch self {
        case .invalidURL: return "URLの構築に失敗しました"
        case .invalidResponse: return "サーバーからの応答が不正です"
        case .httpError(let status, _): return "通信エラー(HTTP \(status))"
        case .decodingFailed: return "レスポンスの解析に失敗しました"
        }
    }
}

final class APIClient {
    static let shared = APIClient()

    private let session: URLSession

    init(session: URLSession = .shared) {
        self.session = session
    }

    func request<T: Decodable>(_ endpoint: APIEndpoint) async throws -> T {
        let urlRequest = try makeURLRequest(endpoint)
        let (data, response) = try await session.data(for: urlRequest)
        try validate(response: response, data: data)
        do {
            return try JSONCoders.decoder.decode(T.self, from: data)
        } catch {
            throw AppError.decodingFailed(underlying: error)
        }
    }

    func requestVoid(_ endpoint: APIEndpoint) async throws {
        let urlRequest = try makeURLRequest(endpoint)
        let (data, response) = try await session.data(for: urlRequest)
        try validate(response: response, data: data)
    }

    private func makeURLRequest(_ endpoint: APIEndpoint) throws -> URLRequest {
        guard var components = URLComponents(
            url: AppConfig.baseURL,
            resolvingAgainstBaseURL: false
        ) else {
            throw AppError.invalidURL
        }
        components.path = components.path + endpoint.path
        components.queryItems = endpoint.queryItems

        guard let url = components.url else {
            throw AppError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.httpBody = endpoint.body
        if endpoint.body != nil {
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        }
        // 認証ヘッダはStep 6でAuthInterceptor経由で付与
        return request
    }

    private func validate(response: URLResponse, data: Data) throws {
        guard let http = response as? HTTPURLResponse else {
            throw AppError.invalidResponse
        }
        guard (200..<300).contains(http.statusCode) else {
            throw AppError.httpError(statusCode: http.statusCode, body: data)
        }
    }
}
