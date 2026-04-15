import {
  Anchor,
  Badge,
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

  if (isLoading) return <Loader m="md" />
  if (error) return <Text c="red" m="md">エラー: {String(error)}</Text>

  const isComplete = (l: { last_year: number; last_month: number }) =>
    year > l.last_year || (year === l.last_year && month > l.last_month)

  return (
    <Container size="xl" py="md">
      <MonthNav year={year} month={month} basePath="/loans" />
      <Group justify="space-between" mb="md">
        <Title order={2}>ローン一覧</Title>
        <Button
          color="grape"
          onClick={() => navigate(`/loans/${year}/${month}/new`)}
        >
          新規作成
        </Button>
      </Group>

      <Table striped highlightOnHover withTableBorder>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>名称</Table.Th>
            <Table.Th>支払日</Table.Th>
            <Table.Th>開始</Table.Th>
            <Table.Th>終了</Table.Th>
            <Table.Th>方法</Table.Th>
            <Table.Th ta="right">初回</Table.Th>
            <Table.Th ta="right">2回目以降</Table.Th>
            <Table.Th>状態</Table.Th>
            <Table.Th>完了</Table.Th>
            <Table.Th>操作</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {loans.map((l) => {
            const complete = isComplete(l)
            return (
              <Table.Tr
                key={l.id}
                style={complete ? { opacity: 0.5 } : undefined}
              >
                <Table.Td>{l.name}</Table.Td>
                <Table.Td>{l.pay_day}</Table.Td>
                <Table.Td>
                  {l.first_year}/{l.first_month}
                </Table.Td>
                <Table.Td>
                  {l.last_year}/{l.last_month}
                </Table.Td>
                <Table.Td>{l.method_name}</Table.Td>
                <Table.Td ta="right">{l.formed_amount_first}</Table.Td>
                <Table.Td ta="right">{l.formed_amount_from_second}</Table.Td>
                <Table.Td>{l.state_label}</Table.Td>
                <Table.Td>
                  {complete ? <Badge color="gray">完了</Badge> : '-'}
                </Table.Td>
                <Table.Td>
                  <Group gap="xs">
                    <Anchor
                      component={Link}
                      to={`/loans/${year}/${month}/${l.id}/edit`}
                      size="sm"
                    >
                      編集
                    </Anchor>
                    <Button
                      size="xs"
                      color="red"
                      variant="subtle"
                      onClick={() => {
                        if (confirm(`「${l.name}」を削除しますか?`))
                          delMut.mutate(l.id)
                      }}
                    >
                      削除
                    </Button>
                  </Group>
                </Table.Td>
              </Table.Tr>
            )
          })}
          {loans.length === 0 && (
            <Table.Tr>
              <Table.Td colSpan={10} ta="center" c="dimmed">
                データがありません
              </Table.Td>
            </Table.Tr>
          )}
        </Table.Tbody>
      </Table>
    </Container>
  )
}
