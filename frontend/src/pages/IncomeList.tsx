import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate, useParams } from 'react-router-dom'
import MonthNav from '../components/MonthNav'
import {
  addDefaultIncomes,
  deleteIncome,
  fetchIncomes,
} from '../api/incomes'

export default function IncomeList() {
  const { year: y, month: m } = useParams<{ year: string; month: string }>()
  const year = Number(y)
  const month = Number(m)
  const qc = useQueryClient()
  const navigate = useNavigate()

  const key = ['incomes', year, month]
  const { data: incomes = [], isLoading, error } = useQuery({
    queryKey: key,
    queryFn: () => fetchIncomes(year, month),
  })

  const delMut = useMutation({
    mutationFn: (id: number) => deleteIncome(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: key }),
    onError: (e: unknown) => alert('削除失敗: ' + extractError(e)),
  })

  const addDefMut = useMutation({
    mutationFn: () => addDefaultIncomes(year, month),
    onSuccess: (d) => {
      alert(`${d.added}件追加しました`)
      qc.invalidateQueries({ queryKey: key })
    },
    onError: (e: unknown) => alert('追加失敗: ' + extractError(e)),
  })

  const total = incomes.reduce((s, i) => s + i.amount, 0)

  if (isLoading) return <p>読み込み中...</p>
  if (error) return <p style={{ color: 'red' }}>エラー: {String(error)}</p>

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <MonthNav year={year} month={month} basePath="/incomes" />
      <h1>収入一覧</h1>
      <p>
        <button onClick={() => navigate(`/incomes/${year}/${month}/new`)}>
          新規作成
        </button>{' '}
        <button
          onClick={() => {
            if (confirm('デフォルトから追加しますか?')) addDefMut.mutate()
          }}
          disabled={addDefMut.isPending}
        >
          デフォルトから追加
        </button>
      </p>

      <table border={1} cellPadding={6} style={{ borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>支払日</th>
            <th>名称</th>
            <th>方法</th>
            <th>口座</th>
            <th>金額</th>
            <th>状態</th>
            <th>操作</th>
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
              <td>
                <Link to={`/incomes/${year}/${month}/${i.id}/edit`}>編集</Link>{' '}
                <button
                  onClick={() => {
                    if (confirm(`「${i.name}」を削除しますか?`))
                      delMut.mutate(i.id)
                  }}
                >
                  削除
                </button>
              </td>
            </tr>
          ))}
          {incomes.length === 0 && (
            <tr>
              <td colSpan={7} style={{ textAlign: 'center', color: '#888' }}>
                データがありません
              </td>
            </tr>
          )}
        </tbody>
      </table>
      <p>
        合計: ¥{total.toLocaleString()} ({incomes.length}件)
      </p>
    </div>
  )
}

function extractError(e: unknown): string {
  type AxiosLike = { response?: { data?: unknown }; message?: string }
  const ax = e as AxiosLike
  if (ax?.response?.data) return JSON.stringify(ax.response.data)
  return ax?.message ?? String(e)
}
