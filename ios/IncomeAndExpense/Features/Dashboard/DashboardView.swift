import SwiftUI

struct DashboardView: View {
    @State private var viewModel = DashboardViewModel()
    private let monthStore = MonthStore.shared

    private let columns = [GridItem(.flexible()), GridItem(.flexible())]

    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                LazyVGrid(columns: columns, spacing: 12) {
                    SummaryCard(title: "収入", amount: viewModel.currentIncome, tint: .green)
                    SummaryCard(title: "支出", amount: viewModel.currentExpense, tint: .red)
                    SummaryCard(title: "前月繰越", amount: viewModel.prevBalance, tint: .secondary)
                    SummaryCard(
                        title: "今月収支",
                        amount: viewModel.currentBalance,
                        tint: viewModel.currentBalance >= 0 ? .green : .red
                    )
                }
                .padding(.horizontal)

                VStack(alignment: .leading, spacing: 8) {
                    Text("収支トレンド (12ヶ月)")
                        .font(.headline)
                        .padding(.horizontal)
                    TrendChart(months: viewModel.trends)
                        .frame(height: 220)
                        .padding(.horizontal)
                        .padding(.bottom)
                        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 12))
                        .padding(.horizontal)
                }

                if let error = viewModel.errorMessage {
                    Text(error)
                        .font(.footnote)
                        .foregroundStyle(.red)
                        .padding(.horizontal)
                }
            }
            .padding(.vertical)
        }
        .refreshable {
            await viewModel.fetch(year: monthStore.year, month: monthStore.month)
        }
        .task(id: monthKey) {
            await viewModel.fetch(year: monthStore.year, month: monthStore.month)
        }
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .principal) {
                MonthPicker(store: monthStore)
            }
        }
    }

    private var monthKey: String { "\(monthStore.year)-\(monthStore.month)" }
}
