import SwiftUI

struct BalanceView: View {
    @State private var viewModel = BalanceViewModel()
    private let monthStore = MonthStore.shared

    var body: some View {
        List {
            Section("残高サマリ") {
                LabeledContent("口座合計") {
                    Text(verbatim: amountText(viewModel.response?.balanceSum))
                        .font(.body.monospacedDigit())
                }
                LabeledContent("計算上の残高") {
                    Text(verbatim: amountText(viewModel.response?.balanceOnDb))
                        .font(.body.monospacedDigit())
                }
                LabeledContent("差額") {
                    diffView(viewModel.response?.balanceDiff ?? 0)
                }
            }

            Section("口座別") {
                if let accounts = viewModel.response?.accounts, !accounts.isEmpty {
                    ForEach(accounts) { account in
                        HStack {
                            VStack(alignment: .leading, spacing: 2) {
                                Text(account.bank).font(.body)
                                Text(account.user).font(.caption).foregroundStyle(.secondary)
                            }
                            Spacer()
                            Text(account.formedBalance)
                                .font(.body.monospacedDigit())
                        }
                    }
                } else {
                    PlaceholderRow(kind: viewModel.isLoading
                        ? .loading
                        : .empty(icon: "building.columns", message: "口座がありません"))
                }
            }

            if let error = viewModel.errorMessage {
                Section {
                    Text(error)
                        .font(.footnote)
                        .foregroundStyle(.red)
                }
            }
        }
        .refreshable {
            await viewModel.fetch(year: monthStore.year, month: monthStore.month)
        }
        .task(id: monthKey) {
            await viewModel.fetch(year: monthStore.year, month: monthStore.month)
        }
        .navigationTitle("残高")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .principal) {
                MonthPicker(store: monthStore)
            }
        }
    }

    private var monthKey: String { "\(monthStore.year)-\(monthStore.month)" }

    private func diffView(_ diff: Int) -> some View {
        Text(verbatim: amountText(diff))
            .font(.body.monospacedDigit())
            .foregroundStyle(diff == 0 ? Color.secondary : Palette.expense)
    }

    private func amountText(_ value: Int?) -> String {
        guard let value else { return "-" }
        return "¥\(value.formatted(.number.grouping(.automatic)))"
    }
}
