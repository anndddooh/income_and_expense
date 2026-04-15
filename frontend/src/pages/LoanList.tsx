import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { deleteLoan, fetchLoans } from '../api/loans'

export default function LoanList() {
  const { year: y, month: m } = useParams<{ year: string; month: string }>()
  const year = Number(y)
  const month = Number(m)
  const qc = useQueryClient()
  const navigate = useNavigate()

  const { data: loans = [], isLoading, error } = useQuery({
    queryKey: ['loans'],
    queryFn: fetchLoans,
  })

  const delMut = useMutation({
    mutationFn: (id: number) => deleteLoan(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['loans'] }),
    onError: (e: unknown) => alert('削除失敗: ' + String(e)),
  })

  if (isLoading) return <p>読み込み中...</p>
  if (error) return <p style={{ color: 'red' }}>エラー: {String(error)}</p>

  const isComplete = (l: { last_year: number; last_month: number }) =>
    year > l.last_year || (year === l.last_year && month > l.last_month)

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h1>
        {year}年{month}月 ローン一覧
      </h1>
      <p>
        <Link to="/">← ホーム</Link>{' '}
        <button onClick={() => navigate(`/loans/${year}/${month}/new`)}>
          新規作成
        </button>
      </p>

      <table border={1} cellPadding={6} style={{ borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>名称</th>
            <th>支払日</th>
            <th>開始</th>
            <th>終了</th>
            <th>方法</th>
            <th>初回</th>
            <th>2回目以降</th>
            <th>状態</th>
            <th>完了</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {loans.map((l) => (
            <tr
              key={l.id}
              style={isComplete(l) ? { color: '#999' } : undefined}
            >
              <td>{l.name}</td>
              <td>{l.pay_day}</td>
              <td>
                {l.first_year}/{l.first_month}
              </td>
              <td>
                {l.last_year}/{l.last_month}
              </td>
              <td>{l.method_name}</td>
              <td style={{ textAlign: 'right' }}>{l.formed_amount_first}</td>
              <td style={{ textAlign: 'right' }}>
                {l.formed_amount_from_second}
              </td>
              <td>{l.state_label}</td>
              <td>{isComplete(l) ? '✓' : ''}</td>
              <td>
                <Link to={`/loans/${year}/${month}/${l.id}/edit`}>編集</Link>{' '}
                <button
                  onClick={() => {
                    if (confirm(`「${l.name}」を削除しますか?`))
                      delMut.mutate(l.id)
                  }}
                >
                  削除
                </button>
              </td>
            </tr>
          ))}
          {loans.length === 0 && (
            <tr>
              <td colSpan={10} style={{ textAlign: 'center', color: '#888' }}>
                データがありません
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
