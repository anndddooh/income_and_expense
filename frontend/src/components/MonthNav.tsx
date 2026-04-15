import { ActionIcon, Anchor, Button, Group, Paper, Text } from '@mantine/core'
import { Link, useLocation, useNavigate } from 'react-router-dom'

type Props = {
  year: number
  month: number
  basePath: string // 例: '/incomes'
}

const FEATURES: { path: string; label: string }[] = [
  { path: '/incomes', label: '収入' },
  { path: '/expenses', label: '支出' },
  { path: '/balance', label: '残高' },
  { path: '/loans', label: 'ローン' },
  { path: '/account_require', label: '口座別必要額' },
  { path: '/method_require', label: '方法別必要額' },
]

export default function MonthNav({ year, month, basePath }: Props) {
  const navigate = useNavigate()
  const location = useLocation()

  const shift = (delta: number) => {
    let y = year
    let m = month + delta
    if (m < 1) {
      y -= 1
      m = 12
    } else if (m > 12) {
      y += 1
      m = 1
    }
    navigate(`${basePath}/${y}/${m}`)
  }

  return (
    <Paper withBorder p="sm" mb="md" radius="md">
      <Group justify="space-between" wrap="wrap">
        <Group>
          <ActionIcon
            component={Link}
            to="/"
            variant="subtle"
            aria-label="ホーム"
          >
            🏠
          </ActionIcon>
          <Button
            variant="default"
            size="xs"
            onClick={() => shift(-1)}
          >
            ← 前月
          </Button>
          <Text fw={700}>
            {year}年{month}月
          </Text>
          <Button
            variant="default"
            size="xs"
            onClick={() => shift(1)}
          >
            次月 →
          </Button>
        </Group>
        <Group gap="sm">
          {FEATURES.map((f) => {
            const active = location.pathname.startsWith(f.path)
            return (
              <Anchor
                key={f.path}
                component={Link}
                to={`${f.path}/${year}/${month}`}
                fw={active ? 700 : 400}
                c={active ? 'red' : undefined}
                size="sm"
              >
                {f.label}
              </Anchor>
            )
          })}
        </Group>
      </Group>
    </Paper>
  )
}
