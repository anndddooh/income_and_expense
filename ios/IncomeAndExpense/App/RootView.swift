import SwiftUI

struct RootView: View {
    var body: some View {
        VStack(spacing: 16) {
            Text("収支")
                .font(.largeTitle)
            Text("baseURL")
                .font(.caption)
                .foregroundStyle(.secondary)
            Text(AppConfig.baseURL.absoluteString)
                .font(.footnote.monospaced())
        }
        .padding()
    }
}

#Preview {
    RootView()
}
