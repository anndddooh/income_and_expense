import SwiftUI

struct ExpenseRowView: View {
    let expense: Expense

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(expense.name)
                    .font(.body)
                HStack(spacing: 8) {
                    Text(expense.payDate, format: .dateTime.month().day())
                        .font(.caption)
                        .foregroundStyle(.secondary)
                    Text(expense.methodName)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }
            Spacer()
            VStack(alignment: .trailing, spacing: 4) {
                Text(verbatim: "¥\(expense.amount.formatted(.number.grouping(.automatic)))")
                    .font(.body.monospacedDigit())
                StateBadge(state: expense.state)
            }
        }
    }
}
