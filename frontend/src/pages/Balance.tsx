import {
  Box,
  Button,
  Container,
  Group,
  Loader,
  NumberInput,
  Stack,
  Table,
  Text,
  Title,
} from '@mantine/core'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { useParams } from 'react-router-dom'
import MonthNav from '../components/MonthNav'
import {
  fetchBalance,
  updateAccountBalance,
  type AccountRow,
} from '../api/balance'

export default function Balance() {
  const { year: y, month: m } = useParams<{ year: string; month: string }>()
  const year = Number(y)
  const month = Number(m)
  const qc = useQueryClient()

  const key = ['balance', year, month]
  const { data, isLoading, error } = useQuery({
    queryKey: key,
    queryFn: () => fetchBalance(year, month),
  })

  const [editing, setEditing] = useState<number | null>(null)
  const [draft, setDraft] = useState<number>(0)

  const mut = useMutation({
    mutationFn: ({ id, balance }: { id: number; balance: number }) =>
      updateAccountBalance(id, balance),
    onSuccess: () => {
      setEditing(null)
      qc.invalidateQueries({ queryKey: key })
    },
    onError: (e: unknown) => alert('更新失敗: ' + String(e)),
  })

  if (isLoading) return <Loader m="md" />
  if (error || !data) return <Text c="red" m="md">エラー: {String(error)}</Text>

  const startEdit = (row: AccountRow) => {
    setEditing(row.id)
    setDraft(row.balance)
  }

  return (
    <Container size="lg" py="md">
      <MonthNav year={year} month={month} basePath="/balance" />
      <Title order={2} mb="md">残高</Title>

      <Table striped highlightOnHover withTableBorder>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>ユーザー</Table.Th>
            <Table.Th>銀行</Table.Th>
            <Table.Th ta="right">実残高</Table.Th>
            <Table.Th>操作</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {data.accounts.map((a) => (
            <Table.Tr key={a.id}>
              <Table.Td>{a.user}</Table.Td>
              <Table.Td>{a.bank}</Table.Td>
              <Table.Td ta="right">
                {editing === a.id ? (
                  <NumberInput
                    value={draft}
                    onChange={(v) => setDraft(Number(v))}
                    w={140}
                    hideControls
                  />
                ) : (
                  a.formed_balance
                )}
              </Table.Td>
              <Table.Td>
                {editing === a.id ? (
                  <Group gap="xs">
                    <Button
                      size="xs"
                      color="blue"
                      loading={mut.isPending}
                      onClick={() => mut.mutate({ id: a.id, balance: draft })}
                    >
                      保存
                    </Button>
                    <Button
                      size="xs"
                      variant="default"
                      onClick={() => setEditing(null)}
                    >
                      キャンセル
                    </Button>
                  </Group>
                ) : (
                  <Button size="xs" variant="light" onClick={() => startEdit(a)}>
                    編集
                  </Button>
                )}
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>

      <Box mt="lg">
        <Stack gap={4}>
          <Text>
            実残高合計: <b>¥{data.balance_sum.toLocaleString()}</b>
          </Text>
          <Text>
            DB残高(完了分): <b>¥{data.balance_on_db.toLocaleString()}</b>
          </Text>
          <Text>
            差額:{' '}
            <Text
              span
              fw={700}
              c={data.balance_diff === 0 ? 'green' : 'red'}
            >
              ¥{data.balance_diff.toLocaleString()}
            </Text>
          </Text>
        </Stack>
      </Box>
    </Container>
  )
}
