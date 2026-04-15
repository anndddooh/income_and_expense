import { useState } from 'react'
import { Link } from 'react-router-dom'
import { todayYearMonth } from '../util/date'

export default function Home() {
  const now = todayYearMonth()
  const [year, setYear] = useState(now.year)
  const [month, setMonth] = useState(now.month)

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h1>家計簿</h1>
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

      <ul>
        <li>
          <Link to={`/incomes/${year}/${month}`}>収入一覧</Link>
        </li>
      </ul>
    </div>
  )
}
