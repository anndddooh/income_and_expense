import {
  BadgeDollarSign,
  ChevronLeft,
  ChevronRight,
  CreditCard,
  LayoutDashboard,
  Landmark,
  PiggyBank,
  ReceiptText,
  Wallet,
} from 'lucide-react'
import type { ReactNode } from 'react'
import {
  Link,
  Outlet,
  useLocation,
  useNavigate,
  useParams,
} from 'react-router-dom'
import { Button } from '@/components/ui/button'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInset,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarTrigger,
} from '@/components/ui/sidebar'
import { todayYearMonth } from '@/util/date'

type NavItem = {
  label: string
  path: string // '/incomes' or '' (dashboard)
  icon: ReactNode
  requiresMonth: boolean
}

const MAIN_NAV: NavItem[] = [
  {
    label: 'ダッシュボード',
    path: '',
    icon: <LayoutDashboard className="size-4" />,
    requiresMonth: false,
  },
  {
    label: '収入',
    path: '/incomes',
    icon: <PiggyBank className="size-4" />,
    requiresMonth: true,
  },
  {
    label: '支出',
    path: '/expenses',
    icon: <ReceiptText className="size-4" />,
    requiresMonth: true,
  },
  {
    label: '残高',
    path: '/balance',
    icon: <Wallet className="size-4" />,
    requiresMonth: true,
  },
  {
    label: 'ローン',
    path: '/loans',
    icon: <Landmark className="size-4" />,
    requiresMonth: true,
  },
  {
    label: '口座別必要額',
    path: '/account_require',
    icon: <CreditCard className="size-4" />,
    requiresMonth: true,
  },
  {
    label: '支払方法別必要額',
    path: '/method_require',
    icon: <BadgeDollarSign className="size-4" />,
    requiresMonth: true,
  },
]

function useCurrentYearMonth() {
  const { year, month } = useParams<{ year?: string; month?: string }>()
  const now = todayYearMonth()
  return {
    year: year ? Number(year) : now.year,
    month: month ? Number(month) : now.month,
  }
}

const CURRENT_YEAR = todayYearMonth().year
const YEAR_OPTIONS = Array.from({ length: 11 }, (_, i) => CURRENT_YEAR - 7 + i)
const MONTH_OPTIONS = Array.from({ length: 12 }, (_, i) => i + 1)

export default function AppLayout() {
  const location = useLocation()
  const navigate = useNavigate()
  const { year, month } = useCurrentYearMonth()

  const goTo = (y: number, m: number) => {
    const seg = location.pathname.split('/').filter(Boolean)
    const base = seg[0] ? `/${seg[0]}` : ''
    if (base) {
      navigate(`${base}/${y}/${m}`)
    } else {
      navigate(`/`, { state: { year: y, month: m } })
    }
  }

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
    goTo(y, m)
  }

  return (
    <SidebarProvider>
      <Sidebar collapsible="icon">
        <SidebarHeader>
          <div className="flex items-center gap-2 px-2 py-1">
            <BadgeDollarSign className="size-5" />
            <span className="text-sm font-semibold">家計簿</span>
          </div>
        </SidebarHeader>
        <SidebarContent>
          <SidebarGroup>
            <SidebarGroupLabel>メニュー</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {MAIN_NAV.map((item) => {
                  const to = item.requiresMonth
                    ? `${item.path}/${year}/${month}`
                    : '/'
                  const active = item.path
                    ? location.pathname.startsWith(item.path)
                    : location.pathname === '/'
                  return (
                    <SidebarMenuItem key={item.label}>
                      <SidebarMenuButton
                        asChild
                        isActive={active}
                        tooltip={item.label}
                      >
                        <Link to={to}>
                          {item.icon}
                          <span>{item.label}</span>
                        </Link>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  )
                })}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>
        <SidebarFooter>
          <div className="px-2 py-2 text-xs text-muted-foreground">
            React + DRF
          </div>
        </SidebarFooter>
      </Sidebar>
      <SidebarInset>
        <header className="sticky top-0 z-10 flex h-14 items-center gap-2 border-b bg-background px-4">
          <SidebarTrigger />
          <Separator orientation="vertical" className="h-6" />
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => shift(-1)}
              aria-label="前月"
            >
              <ChevronLeft className="size-4" />
              前月
            </Button>
            <Popover>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  size="sm"
                  className="tabular-nums font-semibold"
                  aria-label="年月を選択"
                >
                  {year}年{month}月
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-3" align="center">
                <div className="flex items-center gap-2">
                  <Select
                    value={String(year)}
                    onValueChange={(v) => goTo(Number(v), month)}
                  >
                    <SelectTrigger className="w-[100px]" aria-label="年">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {YEAR_OPTIONS.map((y) => (
                        <SelectItem key={y} value={String(y)}>
                          {y}年
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Select
                    value={String(month)}
                    onValueChange={(v) => goTo(year, Number(v))}
                  >
                    <SelectTrigger className="w-[80px]" aria-label="月">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {MONTH_OPTIONS.map((m) => (
                        <SelectItem key={m} value={String(m)}>
                          {m}月
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </PopoverContent>
            </Popover>
            <Button
              variant="outline"
              size="sm"
              onClick={() => shift(1)}
              aria-label="次月"
            >
              次月
              <ChevronRight className="size-4" />
            </Button>
          </div>
        </header>
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </SidebarInset>
    </SidebarProvider>
  )
}
