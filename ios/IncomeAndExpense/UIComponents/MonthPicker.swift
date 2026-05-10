import SwiftUI

/// 各タブのツールバーに表示する年月ピッカー。
/// 左右の矢印で前後月、中央の文字をタップで Menu(年/月選択 + 今月)。
struct MonthPicker: View {
    @Bindable var store: MonthStore

    private static let currentYear: Int = {
        var calendar = Calendar(identifier: .gregorian)
        calendar.timeZone = TimeZone(identifier: "Asia/Tokyo") ?? .current
        return calendar.component(.year, from: Date())
    }()

    private var yearRange: [Int] {
        Array((Self.currentYear - 5)...(Self.currentYear + 1))
    }

    var body: some View {
        HStack(spacing: 8) {
            Button {
                store.goToPreviousMonth()
            } label: {
                Image(systemName: "chevron.left")
            }

            Menu {
                Button("今月") { store.resetToCurrent() }
                Picker("年", selection: $store.year) {
                    ForEach(yearRange, id: \.self) { y in
                        Text(verbatim: "\(y)年").tag(y)
                    }
                }
                Picker("月", selection: $store.month) {
                    ForEach(1...12, id: \.self) { m in
                        Text(verbatim: "\(m)月").tag(m)
                    }
                }
            } label: {
                HStack(spacing: 4) {
                    Text(verbatim: "\(store.year)年\(store.month)月")
                        .fontWeight(.semibold)
                    Image(systemName: "chevron.down")
                        .font(.caption)
                }
            }

            Button {
                store.goToNextMonth()
            } label: {
                Image(systemName: "chevron.right")
            }
        }
    }
}
