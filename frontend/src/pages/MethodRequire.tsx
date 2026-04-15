import {
  Button,
  Container,
  Loader,
  Table,
  Text,
  Title,
} from '@mantine/core'
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

  if (isLoading) return <Loader m="md" />
  if (error || !data) return <Text c="red" m="md">エラー: {String(error)}</Text>

  return (
    <Container size="md" py="md">
      <MonthNav year={year} month={month} basePath="/method_require" />
      <Title order={2} mb="md">支払方法別必要金額</Title>

      <Table striped highlightOnHover withTableBorder>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>支払方法</Table.Th>
            <Table.Th ta="right">必要額</Table.Th>
            <Table.Th>操作</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {data.methods.map((m) => (
            <Table.Tr key={m.id}>
              <Table.Td>{m.display_name}</Table.Td>
              <Table.Td ta="right">{m.formed_require}</Table.Td>
              <Table.Td>
                {m.require > 0 && (
                  <Button
                    size="xs"
                    variant="light"
                    loading={doneMut.isPending}
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
                  </Button>
                )}
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>

      <Text mt="lg">
        必要額合計: <b>¥{data.require_sum.toLocaleString()}</b>
      </Text>
    </Container>
  )
}
