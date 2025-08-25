import { Routes, Route, useLocation } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Header from './components/Header'
import Footer from './components/Footer'
import Home from './components/Home'
import SearchResults from './components/SearchResults'
import SpeciesDetail from './components/SpeciesDetail'
import PlantDetail from './components/PlantDetail'
import MothDetail from './components/MothDetail'
import ButterflyDetail from './components/ButterflyDetail'
import BuprestidaeDetail from './components/BuprestidaeDetail'
import LeafbeetleDetail from './components/LeafbeetleDetail'

function App() {
  const location = useLocation()
  const [currentPath, setCurrentPath] = useState(location.pathname)

  useEffect(() => {
    setCurrentPath(location.pathname)
    // ページ遷移時にトップにスクロール
    window.scrollTo(0, 0)
  }, [location])

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<SearchResults />} />
          <Route path="/species/:id" element={<SpeciesDetail />} />
          <Route path="/plant/:plantName" element={<PlantDetail />} />
          <Route path="/moth/:mothName" element={<MothDetail />} />
          <Route path="/butterfly/:butterflyName" element={<ButterflyDetail />} />
          <Route path="/buprestidae/:buprestidaeName" element={<BuprestidaeDetail />} />
          <Route path="/leafbeetle/:leafbeetleName" element={<LeafbeetleDetail />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}

export default App