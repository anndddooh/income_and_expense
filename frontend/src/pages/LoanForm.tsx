import {
  Button,
  Container,
  Group,
  NumberInput,
  Select,
  Stack,
  Text,
  TextInput,
  Title,
} from '@mantine/core'
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

  const setN = (k: keyof LoanInput) => (v: string | number) =>
    setForm({ ...form, [k]: Number(v) })

  return (
    <Container size="sm" py="md">
      <Title order={2} mb="md">
        {isEdit ? 'ローンを編集' : 'ローンを追加'}
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
          <NumberInput
            label="支払日(1-28)"
            required
            min={1}
            max={28}
            value={form.pay_day}
            onChange={setN('pay_day')}
          />
          <Group grow>
            <NumberInput
              label="開始年"
              required
              value={form.first_year}
              onChange={setN('first_year')}
            />
            <NumberInput
              label="開始月"
              required
              min={1}
              max={12}
              value={form.first_month}
              onChange={setN('first_month')}
            />
          </Group>
          <Group grow>
            <NumberInput
              label="終了年"
              required
              value={form.last_year}
              onChange={setN('last_year')}
            />
            <NumberInput
              label="終了月"
              required
              min={1}
              max={12}
              value={form.last_month}
              onChange={setN('last_month')}
            />
          </Group>
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
            label="初回金額"
            required
            min={0}
            value={form.amount_first}
            onChange={setN('amount_first')}
          />
          <NumberInput
            label="2回目以降金額"
            required
            min={0}
            value={form.amount_from_second}
            onChange={setN('amount_from_second')}
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

          {submitError && <Text c="red">エラー: {submitError}</Text>}

          <Group>
            <Button type="submit" loading={mut.isPending} color="grape">
              {isEdit ? '更新' : '追加'}
            </Button>
            <Button
              type="button"
              variant="default"
              onClick={() => navigate(`/loans/${year}/${month}`)}
            >
              キャンセル
            </Button>
          </Group>
        </Stack>
      </form>
    </Container>
  )
}
