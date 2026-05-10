import SwiftUI

struct IncomeListView: View {
    @State private var store = IncomeStore()
    private let monthStore = MonthStore.shared

    var body: some View {
        List {
            Section {
                LabeledContent("前月繰越") {
                    Text(verbatim: "¥\(store.prevBalance.formatted(.number.grouping(.automatic)))")
                        .font(.body.monospacedDigit())
                }
            }

            Section("収入") {
                if store.incomes.isEmpty && !store.isLoading {
                    Text("収入の記録がありません")
                        .foregroundStyle(.secondary)
                        .font(.callout)
                }
                ForEach(store.incomes) { income in
                    IncomeRowView(income: income)
                        .swipeActions(edge: .trailing, allowsFullSwipe: true) {
                            Button(role: .destructive) {
                                Task { try? await store.delete(id: income.id) }
                            } label: {
                                Label("削除", systemImage: "trash")
                            }
                        }
                }
            }

            if let error = store.errorMessage {
                Section {
                    Text(error)
                        .font(.footnote)
                        .foregroundStyle(.red)
                }
            }
        }
        .refreshable {
            await store.fetch(year: monthStore.year, month: monthStore.month)
        }
        .task(id: monthKey) {
            await store.fetch(year: monthStore.year, month: monthStore.month)
        }
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .principal) {
                MonthPicker(store: monthStore)
            }
        }
    }

    private var monthKey: String {
        "\(monthStore.year)-\(monthStore.month)"
    }
}
