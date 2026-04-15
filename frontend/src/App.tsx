import { useEffect, useState } from 'react'
import './App.css'

type Income = {
  id: number
  name: string
  pay_date: string
  method_name: string
  account: { id: number; user: string; bank: string }
  amount: number
  formed_amount: string
  state: number
  state_label: string
  memo: string | null
}

function App() {
  const [year, setYear] = useState(2022)
  const [month, setMonth] = useState(10)
  const [incomes, setIncomes] = useState<Income[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetch(`http://localhost:8000/api/incomes/?year=${year}&month=${month}`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json()
      })
      .then(setIncomes)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false))
  }, [year, month])

  const total = incomes.reduce((sum, i) => sum + i.amount, 0)

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h1>収入一覧</h1>
      <div style={{ marginBottom: 16 }}>
        <label>
          年:{' '}
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(Number(e.target.value))}
            style={{ width: 80 }}
          />
        </label>{' '}
        <label>
          月:{' '}
          <input
            type="number"
            min={1}
            max={12}
            value={month}
            onChange={(e) => setMonth(Number(e.target.value))}
            style={{ width: 60 }}
          />
        </label>
      </div>

      {loading && <p>読み込み中...</p>}
      {error && <p style={{ color: 'red' }}>エラー: {error}</p>}

      {!loading && !error && (
        <>
          <table border={1} cellPadding={6} style={{ borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>支払日</th>
                <th>名称</th>
                <th>方法</th>
                <th>口座</th>
                <th>金額</th>
                <th>状態</th>
              </tr>
            </thead>
            <tbody>
              {incomes.map((i) => (
                <tr key={i.id}>
                  <td>{i.pay_date}</td>
                  <td>{i.name}</td>
                  <td>{i.method_name}</td>
                  <td>
                    {i.account.user} / {i.account.bank}
                  </td>
                  <td style={{ textAlign: 'right' }}>{i.formed_amount}</td>
                  <td>{i.state_label}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p style={{ marginTop: 12 }}>
            合計: ¥{total.toLocaleString()} ({incomes.length}件)
          </p>
        </>
      )}
    </div>
  )
}

export default App