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
import {
  createLoan,
  fetchLoan,
  updateLoan,
  type LoanInput,
} from '@/api/loans'
import { fetchMethods } from '@/api/methods'
import type { StateValue } from '@/api/types'

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
    <div className="max-w-xl">
      <PageHeader title={isEdit ? 'ローンを編集' : 'ローンを追加'} />

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
            <Field label="支払日 (1-28)" htmlFor="f-pay-day">
              <Input
                id="f-pay-day"
                type="number"
                required
                min={1}
                max={28}
                value={form.pay_day}
                onChange={(e) => setN('pay_day')(e.target.value)}
              />
            </Field>
            <div className="grid grid-cols-2 gap-3">
              <Field label="開始年" htmlFor="f-first-year">
                <Input
                  id="f-first-year"
                  type="number"
                  required
                  value={form.first_year}
                  onChange={(e) => setN('first_year')(e.target.value)}
                />
              </Field>
              <Field label="開始月" htmlFor="f-first-month">
                <Input
                  id="f-first-month"
                  type="number"
                  required
                  min={1}
                  max={12}
                  value={form.first_month}
                  onChange={(e) => setN('first_month')(e.target.value)}
                />
              </Field>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Field label="終了年" htmlFor="f-last-year">
                <Input
                  id="f-last-year"
                  type="number"
                  required
                  value={form.last_year}
                  onChange={(e) => setN('last_year')(e.target.value)}
                />
              </Field>
              <Field label="終了月" htmlFor="f-last-month">
                <Input
                  id="f-last-month"
                  type="number"
                  required
                  min={1}
                  max={12}
                  value={form.last_month}
                  onChange={(e) => setN('last_month')(e.target.value)}
                />
              </Field>
            </div>
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
            <Field label="初回金額" htmlFor="f-amount-first">
              <Input
                id="f-amount-first"
                type="number"
                required
                min={0}
                value={form.amount_first}
                onChange={(e) => setN('amount_first')(e.target.value)}
              />
            </Field>
            <Field label="2回目以降金額" htmlFor="f-amount-from-second">
              <Input
                id="f-amount-from-second"
                type="number"
                required
                min={0}
                value={form.amount_from_second}
                onChange={(e) => setN('amount_from_second')(e.target.value)}
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
                onClick={() => navigate(`/loans/${year}/${month}`)}
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
