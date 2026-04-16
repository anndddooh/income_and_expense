import PageHeader from '@/components/PageHeader'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function Dashboard() {
  return (
    <>
      <PageHeader title="ダッシュボード" description="今月のサマリ" />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader>
            <CardDescription>準備中</CardDescription>
            <CardTitle>Dashboard</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Phase 7-D で KPI カードとグラフを実装予定
            </p>
          </CardContent>
        </Card>
      </div>
    </>
  )
}
