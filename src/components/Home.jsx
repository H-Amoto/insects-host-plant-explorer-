import { useState, useEffect } from 'react'

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
      <div className="text-center mb-16">
        <h1 className="text-6xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent mb-6">
          昆虫食草図鑑
        </h1>
        <p className="text-2xl text-gray-700 dark:text-gray-200 mb-4 font-medium">
          7000種以上の蛾・蝶・タマムシ・ハムシと植物の関係を探索
        </p>
        <p className="text-lg text-gray-500 dark:text-gray-400">
          日本最大級の昆虫-植物関係データベース
        </p>
        
        <form onSubmit={handleSearch} className="max-w-3xl mx-auto mb-12">
          <div className="flex shadow-xl rounded-xl">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="昆虫名または植物名で検索..."
              className="search-input"
            />
            <button
              type="submit"
              className="search-button"
            >
              検索
            </button>
          </div>
        </form>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">蛾</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            3000種以上の蛾と食草の関係データ
          </p>
          <a 
            href="/search?category=moth" 
            className="btn-primary inline-block"
          >
            蛾を探索
          </a>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">蝶</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            日本産蝶類の詳細な食草情報
          </p>
          <a 
            href="/search?category=butterfly" 
            className="btn-primary inline-block"
          >
            蝶を探索
          </a>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">タマムシ</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            タマムシ科の生態と食草関係
          </p>
          <a 
            href="/search?category=buprestidae" 
            className="btn-primary inline-block"
          >
            タマムシを探索
          </a>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">ハムシ</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            ハムシ科の多様な食草関係
          </p>
          <a 
            href="/search?category=leafbeetle" 
            className="btn-primary inline-block"
          >
            ハムシを探索
          </a>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">食草</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            植物から昆虫を逆引き検索
          </p>
          <a 
            href="/search?category=plant" 
            className="btn-primary inline-block"
          >
            食草を探索
          </a>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">詳細検索</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            学名、科名、生息地で詳細検索
          </p>
          <a 
            href="/search" 
            className="btn-primary inline-block"
          >
            詳細検索
          </a>
        </div>
      </div>
    </div>
  )
}

export default Home