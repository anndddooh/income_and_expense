import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  createLoan,
  fetchLoan,
  updateLoan,
  type LoanInput,
} from '../api/loans'
import { fetchMethods } from '../api/methods'
import type { StateValue } from '../api/types'

const STATES: { value: StateValue; label: string }[] = [
  { value: 0, label: '未定' },
  { value: 1, label: '確定' },
  { value: 2, label: '完了' },
]

export default function LoanForm() {
  const { year: y, month: m, id } = useParams<{
    year: string
    month: string
    id?: string
  }>()
  const year = Number(y)
  const month = Number(m)
  const isEdit = !!id
  const itemId = id ? Number(id) : undefined
  const navigate = useNavigate()
  const qc = useQueryClient()

  const [form, setForm] = useState<LoanInput>({
    name: '',
    pay_day: 1,
    first_year: year,
    first_month: month,
    last_year: year,
    last_month: month,
    method: 0,
    amount_first: 0,
    amount_from_second: 0,
    state: 0,
  })
  const [submitError, setSubmitError] = useState<string | null>(null)

  const { data: methods = [] } = useQuery({
    queryKey: ['methods'],
    queryFn: fetchMethods,
  })
  const { data: existing } = useQuery({
    queryKey: ['loan', itemId],
    queryFn: () => fetchLoan(itemId!),
    enabled: isEdit,
  })

  useEffect(() => {
    if (existing) {
      setForm({
        name: existing.name,
        pay_day: existing.pay_day,
        first_year: existing.first_year,
        first_month: existing.first_month,
        last_year: existing.last_year,
        last_month: existing.last_month,
        method: existing.method,
        amount_first: existing.amount_first,
        amount_from_second: existing.amount_from_second,
        state: existing.state,
      })
    }
  }, [existing])

  useEffect(() => {
    if (!isEdit && form.method === 0 && methods[0]) {
      setForm((f) => ({ ...f, method: methods[0].id }))
    }
  }, [methods, isEdit, form.method])

  const mut = useMutation({
    mutationFn: () =>
      isEdit ? updateLoan(itemId!, form) : createLoan(form),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['loans'] })
      navigate(`/loans/${year}/${month}`)
    },
    onError: (e: unknown) => {
      type AxiosLike = { response?: { data?: unknown }; message?: string }
      const ax = e as AxiosLike
      setSubmitError(
        ax?.response?.data
          ? JSON.stringify(ax.response.data)
          : ax?.message ?? String(e)
      )
    },
  })

  const setN = (k: keyof LoanInput) => (v: string) =>
    setForm({ ...form, [k]: Number(v) })

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif', maxWidth: 600 }}>
      <h1>{isEdit ? 'ローンを編集' : 'ローンを追加'}</h1>
      <form
        onSubmit={(e) => {
          e.preventDefault()
          setSubmitError(null)
          mut.mutate()
        }}
      >
        <Row label="名称">
          <input
            required
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
        </Row>
        <Row label="支払日(1-28)">
          <input
            type="number"
            required
            min={1}
            max={28}
            value={form.pay_day}
            onChange={(e) => setN('pay_day')(e.target.value)}
          />
        </Row>
        <Row label="開始年月">
          <input
            type="number"
            required
            value={form.first_year}
            onChange={(e) => setN('first_year')(e.target.value)}
            style={{ width: 90 }}
          />{' '}
          <input
            type="number"
            required
            min={1}
            max={12}
            value={form.first_month}
            onChange={(e) => setN('first_month')(e.target.value)}
            style={{ width: 60 }}
          />
        </Row>
        <Row label="終了年月">
          <input
            type="number"
            required
            value={form.last_year}
            onChange={(e) => setN('last_year')(e.target.value)}
            style={{ width: 90 }}
          />{' '}
          <input
            type="number"
            required
            min={1}
            max={12}
            value={form.last_month}
            onChange={(e) => setN('last_month')(e.target.value)}
            style={{ width: 60 }}
          />
        </Row>
        <Row label="方法">
          <select
            required
            value={form.method}
            onChange={(e) => setN('method')(e.target.value)}
          >
            {methods.map((m) => (
              <option key={m.id} value={m.id}>
                {m.display_name}
              </option>
            ))}
          </select>
        </Row>
        <Row label="初回金額">
          <input
            type="number"
            required
            min={0}
            value={form.amount_first}
            onChange={(e) => setN('amount_first')(e.target.value)}
          />
        </Row>
        <Row label="2回目以降金額">
          <input
            type="number"
            required
            min={0}
            value={form.amount_from_second}
            onChange={(e) => setN('amount_from_second')(e.target.value)}
          />
        </Row>
        <Row label="状態">
          <select
            value={form.state}
            onChange={(e) =>
              setForm({ ...form, state: Number(e.target.value) as StateValue })
            }
          >
            {STATES.map((s) => (
              <option key={s.value} value={s.value}>
                {s.label}
              </option>
            ))}
          </select>
        </Row>

        {submitError && <p style={{ color: 'red' }}>エラー: {submitError}</p>}

        <div style={{ marginTop: 16 }}>
          <button type="submit" disabled={mut.isPending}>
            {isEdit ? '更新' : '追加'}
          </button>{' '}
          <button
            type="button"
            onClick={() => navigate(`/loans/${year}/${month}`)}
          >
            キャンセル
          </button>
        </div>
      </form>
    </div>
  )
}

function Row({
  label,
  children,
}: {
  label: string
  children: React.ReactNode
}) {
  return (
    <div style={{ marginBottom: 12 }}>
      <label style={{ display: 'block', fontWeight: 'bold' }}>{label}</label>
      {children}
    </div>
  )
}
