import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  createIncome,
  fetchIncome,
  updateIncome,
} from '../api/incomes'
import { fetchMethods } from '../api/methods'
import type { IncomeInput, StateValue } from '../api/types'

const STATES: { value: StateValue; label: string }[] = [
  { value: 0, label: '未定' },
  { value: 1, label: '確定' },
  { value: 2, label: '完了' },
]

export default function IncomeForm() {
  const { year: y, month: m, id } = useParams<{
    year: string
    month: string
    id?: string
  }>()
  const year = Number(y)
  const month = Number(m)
  const isEdit = !!id
  const incomeId = id ? Number(id) : undefined
  const navigate = useNavigate()
  const qc = useQueryClient()

  const [form, setForm] = useState<IncomeInput>({
    name: '',
    pay_date: `${year}-${String(month).padStart(2, '0')}-01`,
    method: 0,
    amount: 0,
    state: 0,
    memo: '',
  })
  const [submitError, setSubmitError] = useState<string | null>(null)

  const { data: methods = [] } = useQuery({
    queryKey: ['methods'],
    queryFn: fetchMethods,
  })

  const { data: existing } = useQuery({
    queryKey: ['income', incomeId],
    queryFn: () => fetchIncome(incomeId!),
    enabled: isEdit,
  })

  useEffect(() => {
    if (existing) {
      setForm({
        name: existing.name,
        pay_date: existing.pay_date,
        method: existing.method,
        amount: existing.amount,
        state: existing.state,
        memo: existing.memo ?? '',
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
      isEdit ? updateIncome(incomeId!, form) : createIncome(form),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['incomes', year, month] })
      navigate(`/incomes/${year}/${month}`)
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

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif', maxWidth: 600 }}>
      <h1>{isEdit ? '収入を編集' : '収入を追加'}</h1>
      <form
        onSubmit={(e) => {
          e.preventDefault()
          setSubmitError(null)
          mut.mutate()
        }}
      >
        <FormRow label="名称">
          <input
            required
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
        </FormRow>
        <FormRow label="支払日">
          <input
            type="date"
            required
            value={form.pay_date}
            onChange={(e) => setForm({ ...form, pay_date: e.target.value })}
          />
        </FormRow>
        <FormRow label="方法">
          <select
            required
            value={form.method}
            onChange={(e) =>
              setForm({ ...form, method: Number(e.target.value) })
            }
          >
            {methods.map((m) => (
              <option key={m.id} value={m.id}>
                {m.display_name}
              </option>
            ))}
          </select>
        </FormRow>
        <FormRow label="金額">
          <input
            type="number"
            required
            min={0}
            value={form.amount}
            onChange={(e) => setForm({ ...form, amount: Number(e.target.value) })}
          />
        </FormRow>
        <FormRow label="状態">
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
        </FormRow>
        <FormRow label="メモ">
          <textarea
            rows={4}
            value={form.memo ?? ''}
            onChange={(e) => setForm({ ...form, memo: e.target.value })}
          />
        </FormRow>

        {submitError && (
          <p style={{ color: 'red' }}>エラー: {submitError}</p>
        )}

        <div style={{ marginTop: 16 }}>
          <button type="submit" disabled={mut.isPending}>
            {isEdit ? '更新' : '追加'}
          </button>{' '}
          <button
            type="button"
            onClick={() => navigate(`/incomes/${year}/${month}`)}
          >
            キャンセル
          </button>
        </div>
      </form>
    </div>
  )
}

function FormRow({
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
