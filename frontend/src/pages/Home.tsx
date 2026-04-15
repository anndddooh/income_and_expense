import {
  Button,
  Container,
  Group,
  NumberInput,
  SimpleGrid,
  Stack,
  Title,
} from '@mantine/core'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { todayYearMonth } from '../util/date'

const FEATURES: { path: string; label: string; color: string }[] = [
  { path: 'incomes', label: '収入', color: 'teal' },
  { path: 'expenses', label: '支出', color: 'pink' },
  { path: 'balance', label: '残高', color: 'blue' },
  { path: 'loans', label: 'ローン', color: 'grape' },
  { path: 'account_require', label: '口座別必要額', color: 'orange' },
  { path: 'method_require', label: '方法別必要額', color: 'cyan' },
]

export default function Home() {
  const now = todayYearMonth()
  const [year, setYear] = useState(now.year)
  const [month, setMonth] = useState(now.month)

  return (
    <Container size="sm" py="xl">
      <Stack>
        <Title order={1}>家計簿</Title>
        <Group>
          <NumberInput
            label="年"
            value={year}
            onChange={(v) => setYear(Number(v))}
            w={120}
          />
          <NumberInput
            label="月"
            min={1}
            max={12}
            value={month}
            onChange={(v) => setMonth(Number(v))}
            w={80}
          />
        </Group>
        <SimpleGrid cols={{ base: 2, sm: 3 }} spacing="md">
          {FEATURES.map((f) => (
            <Button
              key={f.path}
              component={Link}
              to={`/${f.path}/${year}/${month}`}
              color={f.color}
              size="lg"
              variant="light"
            >
              {f.label}
            </Button>
          ))}
        </SimpleGrid>
      </Stack>
    </Container>
  )
}
