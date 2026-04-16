import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import PageHeader from '@/components/PageHeader'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import {
  createExpense,
  fetchExpense,
  updateExpense,
  type ExpenseInput,
} from '@/api/expenses'
import { fetchMethods } from '@/api/methods'
import type { StateValue } from '@/api/types'

const STATES: { value: StateValue; label: string }[] = [
  { value: 0, label: '未定' },
  { value: 1, label: '確定' },
  { value: 2, label: '完了' },
]

export default function ExpenseForm() {
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

  const [form, setForm] = useState<ExpenseInput>({
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
    queryKey: ['expense', itemId],
    queryFn: () => fetchExpense(itemId!),
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
      isEdit ? updateExpense(itemId!, form) : createExpense(form),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['expenses', year, month] })
      navigate(`/expenses/${year}/${month}`)
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
    <div className="max-w-xl">
      <PageHeader title={isEdit ? '支出を編集' : '支出を追加'} description={`${year}年${month}月`} />

      <Card>
        <CardContent className="pt-6">
          <form
            className="space-y-4"
            onSubmit={(e) => {
              e.preventDefault()
              setSubmitError(null)
              mut.mutate()
            }}
          >
            <Field label="名称" htmlFor="f-name">
              <Input
                id="f-name"
                required
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
            </Field>
            <Field label="支払日" htmlFor="f-pay-date">
              <Input
                id="f-pay-date"
                type="date"
                required
                value={form.pay_date}
                onChange={(e) => setForm({ ...form, pay_date: e.target.value })}
              />
            </Field>
            <Field label="方法" htmlFor="f-method">
              <Select
                value={form.method ? String(form.method) : undefined}
                onValueChange={(v) => setForm({ ...form, method: Number(v) })}
              >
                <SelectTrigger id="f-method">
                  <SelectValue placeholder="選択" />
                </SelectTrigger>
                <SelectContent>
                  {methods.map((m) => (
                    <SelectItem key={m.id} value={String(m.id)}>
                      {m.display_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>
            <Field label="金額" htmlFor="f-amount">
              <Input
                id="f-amount"
                type="number"
                required
                min={0}
                value={form.amount}
                onChange={(e) =>
                  setForm({ ...form, amount: Number(e.target.value) })
                }
              />
            </Field>
            <Field label="状態" htmlFor="f-state">
              <Select
                value={String(form.state)}
                onValueChange={(v) =>
                  setForm({ ...form, state: Number(v) as StateValue })
                }
              >
                <SelectTrigger id="f-state">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {STATES.map((s) => (
                    <SelectItem key={s.value} value={String(s.value)}>
                      {s.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>
            <Field label="メモ" htmlFor="f-memo">
              <Textarea
                id="f-memo"
                rows={4}
                value={form.memo ?? ''}
                onChange={(e) => setForm({ ...form, memo: e.target.value })}
              />
            </Field>

            {submitError && (
              <p className="text-sm text-destructive">エラー: {submitError}</p>
            )}

            <div className="flex gap-2 pt-2">
              <Button type="submit" disabled={mut.isPending}>
                {isEdit ? '更新' : '追加'}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate(`/expenses/${year}/${month}`)}
              >
                キャンセル
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

function Field({
  label,
  htmlFor,
  children,
}: {
  label: string
  htmlFor: string
  children: React.ReactNode
}) {
  return (
    <div className="space-y-1.5">
      <Label htmlFor={htmlFor}>{label}</Label>
      {children}
    </div>
  )
}
