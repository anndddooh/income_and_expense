import SwiftUI

struct LoanRowView: View {
    let loan: Loan

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Text(loan.name)
                    .font(.body)
                    .fontWeight(.medium)
                Spacer()
                StateBadge(state: loan.state)
            }
            HStack(spacing: 8) {
                Text(verbatim: "\(loan.firstYear)/\(loan.firstMonth) → \(loan.lastYear)/\(loan.lastMonth)")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Text(verbatim: "毎月\(loan.payDay)日")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            HStack {
                Text(loan.methodName)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Spacer()
                Text(verbatim: "初回 ¥\(loan.amountFirst.formatted(.number.grouping(.automatic)))")
                    .font(.caption.monospacedDigit())
                Text(verbatim: "/ 2回目以降 ¥\(loan.amountFromSecond.formatted(.number.grouping(.automatic)))")
                    .font(.caption.monospacedDigit())
            }
        }
    }
}
