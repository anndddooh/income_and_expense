import SwiftUI
import Charts

struct TrendChart: View {
    let months: [TrendMonth]

    var body: some View {
        Chart {
            ForEach(months, id: \.self) { m in
                BarMark(
                    x: .value("月", monthLabel(m)),
                    y: .value("円", m.income)
                )
                .foregroundStyle(by: .value("種別", "収入"))
                .position(by: .value("種別", "収入"))

                BarMark(
                    x: .value("月", monthLabel(m)),
                    y: .value("円", m.expense)
                )
                .foregroundStyle(by: .value("種別", "支出"))
                .position(by: .value("種別", "支出"))
            }
        }
        .chartForegroundStyleScale([
            "収入": Color.green,
            "支出": Color.red,
        ])
        .chartLegend(position: .top, alignment: .trailing)
        .chartXAxis {
            AxisMarks { value in
                AxisValueLabel().font(.caption2)
            }
        }
    }

    private func monthLabel(_ m: TrendMonth) -> String {
        "\(m.year % 100)/\(m.month)"
    }
}
