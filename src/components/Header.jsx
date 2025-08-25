
function Header() {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <a href="/" className="text-2xl font-bold text-green-600 dark:text-green-400">
            昆虫食草図鑑
          </a>
          <nav>
            <ul className="flex space-x-4">
              <li>
                <a 
                  href="/" 
                  className="text-gray-600 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400"
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