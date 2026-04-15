import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { useParams } from 'react-router-dom'
import MonthNav from '../components/MonthNav'
import {
  fetchBalance,
  updateAccountBalance,
  type AccountRow,
} from '../api/balance'

export default function Balance() {
  const { year: y, month: m } = useParams<{ year: string; month: string }>()
  const year = Number(y)
  const month = Number(m)
  const qc = useQueryClient()

  const key = ['balance', year, month]
  const { data, isLoading, error } = useQuery({
    queryKey: key,
    queryFn: () => fetchBalance(year, month),
  })

  const [editing, setEditing] = useState<number | null>(null)
  const [draft, setDraft] = useState<number>(0)

  const mut = useMutation({
    mutationFn: ({ id, balance }: { id: number; balance: number }) =>
      updateAccountBalance(id, balance),
    onSuccess: () => {
      setEditing(null)
      qc.invalidateQueries({ queryKey: key })
    },
    onError: (e: unknown) => alert('更新失敗: ' + String(e)),
  })

  if (isLoading) return <p>読み込み中...</p>
  if (error || !data)
    return <p style={{ color: 'red' }}>エラー: {String(error)}</p>

  const startEdit = (row: AccountRow) => {
    setEditing(row.id)
    setDraft(row.balance)
  }

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <MonthNav year={year} month={month} basePath="/balance" />
      <h1>残高</h1>

      <table border={1} cellPadding={6} style={{ borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>ユーザー</th>
            <th>銀行</th>
            <th>実残高</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {data.accounts.map((a) => (
            <tr key={a.id}>
              <td>{a.user}</td>
              <td>{a.bank}</td>
              <td style={{ textAlign: 'right' }}>
                {editing === a.id ? (
                  <input
                    type="number"
                    value={draft}
                    onChange={(e) => setDraft(Number(e.target.value))}
                    style={{ width: 120 }}
                  />
                ) : (
                  a.formed_balance
                )}
              </td>
              <td>
                {editing === a.id ? (
                  <>
                    <button
                      onClick={() =>
                        mut.mutate({ id: a.id, balance: draft })
                      }
                      disabled={mut.isPending}
                    >
                      保存
                    </button>{' '}
                    <button onClick={() => setEditing(null)}>キャンセル</button>
                  </>
                ) : (
                  <button onClick={() => startEdit(a)}>編集</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ marginTop: 16 }}>
        <p>
          実残高合計: <b>¥{data.balance_sum.toLocaleString()}</b>
        </p>
        <p>
          DB残高(完了分): <b>¥{data.balance_on_db.toLocaleString()}</b>
        </p>
        <p>
          差額:{' '}
          <b style={{ color: data.balance_diff === 0 ? 'green' : 'red' }}>
            ¥{data.balance_diff.toLocaleString()}
          </b>
        </p>
      </div>
    </div>
  )
}
