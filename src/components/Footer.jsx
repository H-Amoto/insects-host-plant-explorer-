function Footer() {
  return (
    <footer className="bg-gradient-to-r from-gray-900 to-gray-800 text-white py-12 mt-20">
      <div className="container mx-auto px-6">
        <div className="text-center">
          <h3 className="text-2xl font-bold mb-4 bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
            昆虫食草図鑑
          </h3>
          <p className="text-lg text-gray-300 mb-2">
            &copy; 2025 昆虫食草図鑑. All rights reserved.
          </p>
          <p className="text-gray-400">
            7000種以上の昆虫と食草の関係を網羅した専門データベース
          </p>
          <div className="mt-6 pt-6 border-t border-gray-700">
            <p className="text-sm text-gray-500">
              研究・教育目的での利用を歓迎します
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer