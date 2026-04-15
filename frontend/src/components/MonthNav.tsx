import { Link, useLocation, useNavigate } from 'react-router-dom'

type Props = {
  year: number
  month: number
  basePath: string // 例: '/incomes', '/expenses'
}

/**
 * 前月・次月ボタン + 機能別のリンク群。
 * 現在URLの /:feature/:year/:month 部分を基準に切り替える。
 */
export default function MonthNav({ year, month, basePath }: Props) {
  const navigate = useNavigate()
  const location = useLocation()

  const shift = (delta: number) => {
    let y = year
    let m = month + delta
    if (m < 1) {
      y -= 1
      m = 12
    } else if (m > 12) {
      y += 1
      m = 1
    }
    navigate(`${basePath}/${y}/${m}`)
  }

  const features: { path: string; label: string }[] = [
    { path: '/incomes', label: '収入' },
    { path: '/expenses', label: '支出' },
    { path: '/balance', label: '残高' },
    { path: '/loans', label: 'ローン' },
    { path: '/account_require', label: '口座別必要額' },
    { path: '/method_require', label: '方法別必要額' },
  ]

  return (
    <div
      style={{
        padding: '8px 0',
        borderBottom: '1px solid #ddd',
        marginBottom: 16,
      }}
    >
      <div style={{ marginBottom: 8 }}>
        <Link to="/">🏠</Link>{' '}
        <button onClick={() => shift(-1)}>← 前月</button>{' '}
        <b style={{ margin: '0 8px' }}>
          {year}年{month}月
        </b>
        <button onClick={() => shift(1)}>次月 →</button>
      </div>
      <nav style={{ fontSize: '0.9em' }}>
        {features.map((f) => {
          const active = location.pathname.startsWith(f.path)
          return (
            <Link
              key={f.path}
              to={`${f.path}/${year}/${month}`}
              style={{
                marginRight: 12,
                fontWeight: active ? 'bold' : 'normal',
                color: active ? '#d44' : undefined,
              }}
            >
              {f.label}
            </Link>
          )
        })}
      </nav>
    </div>
  )
}
