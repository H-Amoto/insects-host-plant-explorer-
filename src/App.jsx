import React, { useState } from 'react'
import Home from './components/Home'
import Header from './components/Header'
import Footer from './components/Footer'
import SearchResults from './components/SearchResults'
import SpeciesDetail from './components/SpeciesDetail'
import PlantDetail from './components/PlantDetail'
import MothDetail from './components/MothDetail'
import ButterflyDetail from './components/ButterflyDetail'
import LeafbeetleDetail from './components/LeafbeetleDetail'
import BuprestidaeDetail from './components/BuprestidaeDetail'

function App() {
  const [currentView, setCurrentView] = useState('home')
  const [currentParams, setCurrentParams] = useState({})

  // URLパラメータを解析してビューを設定する関数
  React.useEffect(() => {
    const updateViewFromURL = () => {
      const pathname = window.location.pathname
      const search = window.location.search
      const params = new URLSearchParams(search)

      if (pathname === '/search') {
        setCurrentView('search')
        setCurrentParams({ q: params.get('q') })
      } else if (pathname.startsWith('/species/')) {
        setCurrentView('species')
        setCurrentParams({ id: pathname.split('/')[2] })
      } else if (pathname.startsWith('/plant/')) {
        setCurrentView('plant') 
        setCurrentParams({ name: pathname.split('/')[2] })
      } else if (pathname.startsWith('/moth/')) {
        setCurrentView('moth')
        setCurrentParams({ id: pathname.split('/')[2] })
      } else if (pathname.startsWith('/butterfly/')) {
        setCurrentView('butterfly')
        setCurrentParams({ id: pathname.split('/')[2] })
      } else if (pathname.startsWith('/leafbeetle/')) {
        setCurrentView('leafbeetle')
        setCurrentParams({ id: pathname.split('/')[2] })
      } else if (pathname.startsWith('/buprestidae/')) {
        setCurrentView('buprestidae')
        setCurrentParams({ id: pathname.split('/')[2] })
      } else {
        setCurrentView('home')
        setCurrentParams({})
      }
    }

    updateViewFromURL()
    
    // ブラウザの戻る/進むボタン対応
    window.addEventListener('popstate', updateViewFromURL)
    return () => window.removeEventListener('popstate', updateViewFromURL)
  }, [])

  // ビューに基づいてコンテンツをレンダリング
  const renderContent = () => {
    switch (currentView) {
      case 'search':
        return <SearchResults searchTerm={currentParams.q} />
      case 'species':
        return <SpeciesDetail speciesId={currentParams.id} />
      case 'plant':
        return <PlantDetail plantName={currentParams.name} />
      case 'moth':
        return <MothDetail mothId={currentParams.id} />
      case 'butterfly':
        return <ButterflyDetail butterflyId={currentParams.id} />
      case 'leafbeetle':
        return <LeafbeetleDetail leafbeetleId={currentParams.id} />
      case 'buprestidae':
        return <BuprestidaeDetail buprestidaeId={currentParams.id} />
      default:
        return <Home />
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      <Header />
      <main className="container mx-auto px-4 py-8">
        {renderContent()}
      </main>
      <Footer />
    </div>
  )
}

export default App