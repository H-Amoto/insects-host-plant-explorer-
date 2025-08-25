import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function Home() {
  const [searchTerm, setSearchTerm] = useState('')

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchTerm.trim()) {
      window.location.href = `/search?q=${encodeURIComponent(searchTerm.trim())}`
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">
          昆虫食草図鑑
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
          7000種以上の蛾・蝶・タマムシ・ハムシと植物の関係を探索
        </p>
        
        <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-8">
          <div className="flex">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="昆虫名または植物名で検索..."
              className="flex-1 px-4 py-3 text-lg border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
            />
            <button
              type="submit"
              className="px-6 py-3 bg-green-600 text-white font-semibold rounded-r-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              検索
            </button>
          </div>
        </form>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">蛾</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            3000種以上の蛾と食草の関係データ
          </p>
          <Link 
            to="/search?category=moth" 
            className="btn-primary inline-block"
          >
            蛾を探索
          </Link>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">蝶</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            日本産蝶類の詳細な食草情報
          </p>
          <Link 
            to="/search?category=butterfly" 
            className="btn-primary inline-block"
          >
            蝶を探索
          </Link>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">タマムシ</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            タマムシ科の生態と食草関係
          </p>
          <Link 
            to="/search?category=buprestidae" 
            className="btn-primary inline-block"
          >
            タマムシを探索
          </Link>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">ハムシ</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            ハムシ科の多様な食草関係
          </p>
          <Link 
            to="/search?category=leafbeetle" 
            className="btn-primary inline-block"
          >
            ハムシを探索
          </Link>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">食草</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            植物から昆虫を逆引き検索
          </p>
          <Link 
            to="/search?category=plant" 
            className="btn-primary inline-block"
          >
            食草を探索
          </Link>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">詳細検索</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            学名、科名、生息地で詳細検索
          </p>
          <Link 
            to="/search" 
            className="btn-primary inline-block"
          >
            詳細検索
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Home