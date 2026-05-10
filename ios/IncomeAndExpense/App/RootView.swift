import SwiftUI

struct RootView: View {
    private let authStore = AuthStore.shared

    var body: some View {
        Group {
            if authStore.isLoggedIn {
                LoggedInPlaceholderView()
            } else {
                LoginView()
            }
        }
    }
}

private struct LoggedInPlaceholderView: View {
    var body: some View {
        VStack(spacing: 16) {
            Text("ログイン済み")
                .font(.largeTitle)
            Text("TabView は Step 9 で実装予定")
                .font(.footnote)
                .foregroundStyle(.secondary)
            Button(role: .destructive) {
                AuthStore.shared.logout()
            } label: {
                Text("ログアウト")
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}

#Preview {
    RootView()
}
