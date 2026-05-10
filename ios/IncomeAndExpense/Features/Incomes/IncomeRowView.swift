import SwiftUI

struct IncomeRowView: View {
    let income: Income

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(income.name)
                    .font(.body)
                HStack(spacing: 8) {
                    Text(income.payDate, format: .dateTime.month().day())
                        .font(.caption)
                        .foregroundStyle(.secondary)
                    Text(income.methodName)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }
            Spacer()
            VStack(alignment: .trailing, spacing: 4) {
                Text(verbatim: "¥\(income.amount.formatted(.number.grouping(.automatic)))")
                    .font(.body.monospacedDigit())
                StateBadge(state: income.state)
            }
        }
    }
}
