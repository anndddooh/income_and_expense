import {
  Box,
  Container,
  Loader,
  Stack,
  Table,
  Text,
  Title,
} from '@mantine/core'
import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import MonthNav from '../components/MonthNav'
import { fetchAccountRequire } from '../api/requires'

export default function AccountRequire() {
  const { year: y, month: m } = useParams<{ year: string; month: string }>()
  const year = Number(y)
  const month = Number(m)
  const { data, isLoading, error } = useQuery({
    queryKey: ['account-require', year, month],
    queryFn: () => fetchAccountRequire(year, month),
  })

  if (isLoading) return <Loader m="md" />
  if (error || !data) return <Text c="red" m="md">エラー: {String(error)}</Text>

  return (
    <Container size="lg" py="md">
      <MonthNav year={year} month={month} basePath="/account_require" />
      <Title order={2} mb="md">口座別必要金額</Title>

      <Table striped highlightOnHover withTableBorder>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>ユーザー</Table.Th>
            <Table.Th>銀行</Table.Th>
            <Table.Th ta="right">残高</Table.Th>
            <Table.Th ta="right">必要額</Table.Th>
            <Table.Th ta="right">不足額</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {data.accounts.map((a) => (
            <Table.Tr
              key={a.id}
              bg={a.is_insufficient ? 'red.0' : undefined}
            >
              <Table.Td>{a.user}</Table.Td>
              <Table.Td>{a.bank}</Table.Td>
              <Table.Td ta="right">{a.formed_balance}</Table.Td>
              <Table.Td ta="right">{a.formed_require}</Table.Td>
              <Table.Td ta="right">
                {a.is_insufficient ? (
                  <Text span c="red" fw={700}>
                    {a.formed_insufficient}
                  </Text>
                ) : (
                  '-'
                )}
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>

      <Box mt="lg">
        <Stack gap={4}>
          <Text>
            必要額合計: <b>¥{data.require_sum.toLocaleString()}</b>
          </Text>
          <Text>
            不足額合計:{' '}
            <Text span fw={700} c={data.insufficient_sum > 0 ? 'red' : 'green'}>
              ¥{data.insufficient_sum.toLocaleString()}
            </Text>
          </Text>
        </Stack>
      </Box>
    </Container>
  )
}
