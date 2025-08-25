
function Header() {
  return (
    <header className="bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm shadow-xl border-b border-gray-100 dark:border-gray-800 sticky top-0 z-50">
      <div className="container mx-auto px-6 py-6">
        <div className="flex items-center justify-between">
          <a href="/" className="text-3xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent hover:from-green-700 hover:to-blue-700 transition-colors">
            昆虫食草図鑑
          </a>
          <nav>
            <ul className="flex space-x-6">
              <li>
                <a 
                  href="/" 
                  className="text-gray-700 dark:text-gray-200 hover:text-green-600 dark:hover:text-green-400 font-medium px-4 py-2 rounded-lg hover:bg-green-50 dark:hover:bg-green-900/20 transition-all"
                >
                  ホーム
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header