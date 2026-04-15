import {
  Button,
  Container,
  Group,
  NumberInput,
  Select,
  Stack,
  Text,
  TextInput,
  Textarea,
  Title,
} from '@mantine/core'
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
    <Container size="sm" py="md">
      <Title order={2} mb="md">
        {isEdit ? '収入を編集' : '収入を追加'}
      </Title>
      <form
        onSubmit={(e) => {
          e.preventDefault()
          setSubmitError(null)
          mut.mutate()
        }}
      >
        <Stack>
          <TextInput
            label="名称"
            required
            value={form.name}
            onChange={(e) =>
              setForm({ ...form, name: e.currentTarget.value })
            }
          />
          <TextInput
            label="支払日"
            type="date"
            required
            value={form.pay_date}
            onChange={(e) =>
              setForm({ ...form, pay_date: e.currentTarget.value })
            }
          />
          <Select
            label="方法"
            required
            data={methods.map((m) => ({
              value: String(m.id),
              label: m.display_name,
            }))}
            value={form.method ? String(form.method) : null}
            onChange={(v) => setForm({ ...form, method: Number(v) })}
          />
          <NumberInput
            label="金額"
            required
            min={0}
            value={form.amount}
            onChange={(v) => setForm({ ...form, amount: Number(v) })}
          />
          <Select
            label="状態"
            data={STATES.map((s) => ({
              value: String(s.value),
              label: s.label,
            }))}
            value={String(form.state)}
            onChange={(v) =>
              setForm({ ...form, state: Number(v) as StateValue })
            }
          />
          <Textarea
            label="メモ"
            rows={4}
            value={form.memo ?? ''}
            onChange={(e) =>
              setForm({ ...form, memo: e.currentTarget.value })
            }
          />

          {submitError && <Text c="red">エラー: {submitError}</Text>}

          <Group>
            <Button type="submit" loading={mut.isPending} color="teal">
              {isEdit ? '更新' : '追加'}
            </Button>
            <Button
              type="button"
              variant="default"
              onClick={() => navigate(`/incomes/${year}/${month}`)}
            >
              キャンセル
            </Button>
          </Group>
        </Stack>
      </form>
    </Container>
  )
}
