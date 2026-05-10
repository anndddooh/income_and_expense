import Foundation

enum TemplateDateType: String, Codable {
    case today
    case later
}

struct TemplateExpense: Codable, Identifiable, Hashable {
    let id: Int
    let templateName: String
    let name: String
    let dateType: TemplateDateType
    let payDay: Int
    let limitDayOfThisMonth: Int
    let method: Int
    let methodName: String
    let state: InexState
    let payDate: Date

    enum CodingKeys: String, CodingKey {
        case id, name, method, state
        case templateName = "template_name"
        case dateType = "date_type"
        case payDay = "pay_day"
        case limitDayOfThisMonth = "limit_day_of_this_month"
        case methodName = "method_name"
        case payDate = "pay_date"
    }
}
