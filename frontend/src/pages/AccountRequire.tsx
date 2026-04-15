import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import MonthNav from '../components/MonthNav'
import { fetchAccountRequire } from '../api/requires'

export default function AccountRequire() {
  const { year: y, month: m } = useParams<{ year: string; month: string }>()
  const year = Number(y)
  const month = Number(m)
  const { data, isLoading, error } = useQuery({
    queryKey: ['account-require', year, month],
    queryFn: () => fetchAccountRequire(year, month),
  })

  if (isLoading) return <p>読み込み中...</p>
  if (error || !data)
    return <p style={{ color: 'red' }}>エラー: {String(error)}</p>

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <MonthNav year={year} month={month} basePath="/account_require" />
      <h1>口座別必要金額</h1>

      <table border={1} cellPadding={6} style={{ borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>ユーザー</th>
            <th>銀行</th>
            <th>残高</th>
            <th>必要額</th>
            <th>不足額</th>
          </tr>
        </thead>
        <tbody>
          {data.accounts.map((a) => (
            <tr
              key={a.id}
              style={
                a.is_insufficient
                  ? { backgroundColor: '#fee' }
                  : undefined
              }
            >
              <td>{a.user}</td>
              <td>{a.bank}</td>
              <td style={{ textAlign: 'right' }}>{a.formed_balance}</td>
              <td style={{ textAlign: 'right' }}>{a.formed_require}</td>
              <td style={{ textAlign: 'right' }}>
                {a.is_insufficient ? a.formed_insufficient : '-'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ marginTop: 16 }}>
        <p>
          必要額合計: <b>¥{data.require_sum.toLocaleString()}</b>
        </p>
        <p>
          不足額合計:{' '}
          <b style={{ color: data.insufficient_sum > 0 ? 'red' : 'green' }}>
            ¥{data.insufficient_sum.toLocaleString()}
          </b>
        </p>
      </div>
    </div>
  )
}
