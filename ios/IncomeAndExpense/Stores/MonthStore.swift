import Foundation
import Observation

@Observable
final class MonthStore {
    static let shared = MonthStore()

    var year: Int
    var month: Int

    private init() {
        var calendar = Calendar(identifier: .gregorian)
        calendar.timeZone = TimeZone(identifier: "Asia/Tokyo") ?? .current
        let comps = calendar.dateComponents([.year, .month], from: Date())
        self.year = comps.year ?? 2026
        self.month = comps.month ?? 1
    }

    func goToPreviousMonth() {
        if month == 1 {
            month = 12
            year -= 1
        } else {
            month -= 1
        }
    }

    func goToNextMonth() {
        if month == 12 {
            month = 1
            year += 1
        } else {
            month += 1
        }
    }

    func resetToCurrent() {
        var calendar = Calendar(identifier: .gregorian)
        calendar.timeZone = TimeZone(identifier: "Asia/Tokyo") ?? .current
        let comps = calendar.dateComponents([.year, .month], from: Date())
        year = comps.year ?? year
        month = comps.month ?? month
    }
}
