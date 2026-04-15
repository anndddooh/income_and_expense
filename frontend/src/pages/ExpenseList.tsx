import {
  Anchor,
  Button,
  Container,
  Group,
  Loader,
  Table,
  Text,
  Title,
} from '@mantine/core'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate, useParams } from 'react-router-dom'
import MonthNav from '../components/MonthNav'
import {
  addDefaultExpenses,
  deleteExpense,
  fetchExpenses,
} from '../api/expenses'

export default function ExpenseList() {
  const { year: y, month: m } = useParams<{ year: string; month: string }>()
  const year = Number(y)
  const month = Number(m)
  const qc = useQueryClient()
  const navigate = useNavigate()

  const key = ['expenses', year, month]
  const { data: items = [], isLoading, error } = useQuery({
    queryKey: key,
    queryFn: () => fetchExpenses(year, month),
  })

  const delMut = useMutation({
    mutationFn: (id: number) => deleteExpense(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: key }),
    onError: (e: unknown) => alert('削除失敗: ' + extractError(e)),
  })

  const addDefMut = useMutation({
    mutationFn: () => addDefaultExpenses(year, month),
    onSuccess: (d) => {
      alert(`${d.added}件追加しました`)
      qc.invalidateQueries({ queryKey: key })
    },
    onError: (e: unknown) => alert('追加失敗: ' + extractError(e)),
  })

  const total = items.reduce((s, i) => s + i.amount, 0)

  if (isLoading) return <Loader m="md" />
  if (error) return <Text c="red" m="md">エラー: {String(error)}</Text>

  return (
    <Container size="lg" py="md">
      <MonthNav year={year} month={month} basePath="/expenses" />
      <Group justify="space-between" mb="md">
        <Title order={2}>支出一覧</Title>
        <Group>
          <Button
            color="pink"
            onClick={() => navigate(`/expenses/${year}/${month}/new`)}
          >
            新規作成
          </Button>
          <Button
            variant="light"
            loading={addDefMut.isPending}
            onClick={() => {
              if (confirm('デフォルト/ローンから追加しますか?')) addDefMut.mutate()
            }}
          >
            デフォルトから追加
          </Button>
        </Group>
      </Group>

      <Table striped highlightOnHover withTableBorder>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>支払日</Table.Th>
            <Table.Th>名称</Table.Th>
            <Table.Th>方法</Table.Th>
            <Table.Th>口座</Table.Th>
            <Table.Th ta="right">金額</Table.Th>
            <Table.Th>状態</Table.Th>
            <Table.Th>操作</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {items.map((i) => (
            <Table.Tr key={i.id}>
              <Table.Td>{i.pay_date}</Table.Td>
              <Table.Td>{i.name}</Table.Td>
              <Table.Td>{i.method_name}</Table.Td>
              <Table.Td>
                {i.account.user} / {i.account.bank}
              </Table.Td>
              <Table.Td ta="right">{i.formed_amount}</Table.Td>
              <Table.Td>{i.state_label}</Table.Td>
              <Table.Td>
                <Group gap="xs">
                  <Anchor
                    component={Link}
                    to={`/expenses/${year}/${month}/${i.id}/edit`}
                    size="sm"
                  >
                    編集
                  </Anchor>
                  <Button
                    size="xs"
                    color="red"
                    variant="subtle"
                    onClick={() => {
                      if (confirm(`「${i.name}」を削除しますか?`))
                        delMut.mutate(i.id)
                    }}
                  >
                    削除
                  </Button>
                </Group>
              </Table.Td>
            </Table.Tr>
          ))}
          {items.length === 0 && (
            <Table.Tr>
              <Table.Td colSpan={7} ta="center" c="dimmed">
                データがありません
              </Table.Td>
            </Table.Tr>
          )}
        </Table.Tbody>
      </Table>
      <Text mt="md">
        合計: <b>¥{total.toLocaleString()}</b> ({items.length}件)
      </Text>
    </Container>
  )
}

function extractError(e: unknown): string {
  type AxiosLike = { response?: { data?: unknown }; message?: string }
  const ax = e as AxiosLike
  if (ax?.response?.data) return JSON.stringify(ax.response.data)
  return ax?.message ?? String(e)
}
