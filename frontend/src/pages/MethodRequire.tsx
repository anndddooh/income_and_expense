import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import MonthNav from '../components/MonthNav'
import { fetchMethodRequire, methodDone } from '../api/requires'

export default function MethodRequire() {
  const { year: y, month: m } = useParams<{ year: string; month: string }>()
  const year = Number(y)
  const month = Number(m)
  const qc = useQueryClient()
  const key = ['method-require', year, month]

  const { data, isLoading, error } = useQuery({
    queryKey: key,
    queryFn: () => fetchMethodRequire(year, month),
  })

  const doneMut = useMutation({
    mutationFn: (id: number) => methodDone(id, year, month),
    onSuccess: (d) => {
      alert(`${d.updated}件を完了にしました`)
      qc.invalidateQueries({ queryKey: key })
    },
    onError: (e: unknown) => alert('失敗: ' + String(e)),
  })

  if (isLoading) return <p>読み込み中...</p>
  if (error || !data)
    return <p style={{ color: 'red' }}>エラー: {String(error)}</p>

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <MonthNav year={year} month={month} basePath="/method_require" />
      <h1>支払方法別必要金額</h1>

      <table border={1} cellPadding={6} style={{ borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>支払方法</th>
            <th>必要額</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {data.methods.map((m) => (
            <tr key={m.id}>
              <td>{m.display_name}</td>
              <td style={{ textAlign: 'right' }}>{m.formed_require}</td>
              <td>
                {m.require > 0 && (
                  <button
                    disabled={doneMut.isPending}
                    onClick={() => {
                      if (
                        confirm(
                          `${m.display_name} の未完了支出を全て完了にしますか?`
                        )
                      )
                        doneMut.mutate(m.id)
                    }}
                  >
                    一括完了
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <p style={{ marginTop: 16 }}>
        必要額合計: <b>¥{data.require_sum.toLocaleString()}</b>
      </p>
    </div>
  )
}
