import React, { useState } from 'react';

/**
 * 観察タイプ別のアイコンとスタイルを取得
 */
const getObservationTypeStyle = (observationType) => {
  switch (observationType) {
    case '飼育':
      return {
        icon: '🔬',
        label: '飼育',
        bgColor: 'bg-blue-50 dark:bg-blue-900/20',
        textColor: 'text-blue-700 dark:text-blue-300',
        borderColor: 'border-blue-200 dark:border-blue-700'
      };
    case '野外（国内）':
      return {
        icon: '🌿',
        label: '野外',
        bgColor: 'bg-green-50 dark:bg-green-900/20',
        textColor: 'text-green-700 dark:text-green-300',
        borderColor: 'border-green-200 dark:border-green-700'
      };
    case '海外':
      return {
        icon: '🌍',
        label: '海外',
        bgColor: 'bg-purple-50 dark:bg-purple-900/20',
        textColor: 'text-purple-700 dark:text-purple-300',
        borderColor: 'border-purple-200 dark:border-purple-700'
      };
    default:
      return {
        icon: '📝',
        label: '記録',
        bgColor: 'bg-gray-50 dark:bg-gray-900/20',
        textColor: 'text-gray-700 dark:text-gray-300',
        borderColor: 'border-gray-200 dark:border-gray-700'
      };
  }
};

/**
 * 利用部位のアイコンを取得
 */
const getPlantPartIcon = (plantPart) => {
  switch (plantPart) {
    case '葉': return '🍃';
    case '花': return '🌸';
    case '果実': return '🍓';
    case '樹皮': return '🌳';
    case '根': return '🌱';
    case '全体': return '🌿';
    case '枯葉': return '🍂';
    case '菌類': return '🍄';
    default: return '🍃';
  }
};

/**
 * 利用ステージのアイコンを取得
 */
const getLifeStageIcon = (lifeStage) => {
  switch (lifeStage) {
    case '成虫': return '🦋';
    case '幼虫': return '🐛';
    case '両方': return '🔄';
    default: return '🐛';
  }
};

/**
 * 個別食草情報の詳細表示コンポーネント
 */
const HostPlantDetailCard = ({ hostPlant, isExpanded, onToggle }) => {
  const obsStyle = getObservationTypeStyle(hostPlant.observationType);
  
  // 「野外（国内）」以外の記録は透明度を下げて区別
  const isDomesticWild = hostPlant.observationType === '野外（国内）';
  const cardOpacity = isDomesticWild ? 'opacity-100' : 'opacity-75';
  const cardFilter = isDomesticWild ? '' : 'saturate-75';
  
  return (
    <div className={`rounded-lg border ${obsStyle.borderColor} ${obsStyle.bgColor} p-3 transition-all duration-200 ${cardOpacity} ${cardFilter}`}>
      {/* 基本情報行 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2 flex-1 min-w-0">
          <span className="text-lg">{obsStyle.icon}</span>
          <div className="flex-1 min-w-0">
            <span className={`font-medium ${isDomesticWild ? 'text-slate-800 dark:text-slate-200' : 'text-slate-600 dark:text-slate-400'}`}>
              {hostPlant.name}
            </span>
            {hostPlant.family && (
              <span className={`text-sm ml-1 ${isDomesticWild ? 'text-slate-600 dark:text-slate-400' : 'text-slate-500 dark:text-slate-500'}`}>
                （{hostPlant.family}）
              </span>
            )}
          </div>
          <span className={`text-xs px-2 py-1 rounded-full ${obsStyle.bgColor} ${obsStyle.textColor} font-medium`}>
            {obsStyle.label}
          </span>
        </div>
        
        {/* 詳細情報がある場合のトグルボタン */}
        {(hostPlant.plantPart || hostPlant.lifeStage || hostPlant.reference || hostPlant.notes) && (
          <button
            onClick={onToggle}
            className="ml-2 p-1 rounded-full hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            aria-label={isExpanded ? "詳細を閉じる" : "詳細を表示"}
          >
            <svg 
              className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        )}
      </div>
      
      {/* 詳細情報（展開時） */}
      {isExpanded && (
        <div className="mt-3 pt-3 border-t border-slate-200 dark:border-slate-600 space-y-2">
          {/* 利用情報 */}
          {(hostPlant.plantPart || hostPlant.lifeStage) && (
            <div className="flex items-center space-x-4 text-sm">
              {hostPlant.plantPart && (
                <div className="flex items-center space-x-1">
                  <span>{getPlantPartIcon(hostPlant.plantPart)}</span>
                  <span className="text-slate-600 dark:text-slate-400">部位:</span>
                  <span className="font-medium">{hostPlant.plantPart}</span>
                </div>
              )}
              {hostPlant.lifeStage && (
                <div className="flex items-center space-x-1">
                  <span>{getLifeStageIcon(hostPlant.lifeStage)}</span>
                  <span className="text-slate-600 dark:text-slate-400">利用:</span>
                  <span className="font-medium">{hostPlant.lifeStage}</span>
                </div>
              )}
            </div>
          )}
          
          {/* 出典情報 */}
          {hostPlant.reference && (
            <div className="flex items-start space-x-1 text-sm">
              <span className="text-slate-600 dark:text-slate-400 mt-0.5">📚</span>
              <div>
                <span className="text-slate-600 dark:text-slate-400">出典:</span>
                <span className="ml-1 font-medium text-slate-700 dark:text-slate-300">
                  {hostPlant.reference}
                </span>
              </div>
            </div>
          )}
          
          {/* 備考 */}
          {hostPlant.notes && (
            <div className="flex items-start space-x-1 text-sm">
              <span className="text-slate-600 dark:text-slate-400 mt-0.5">💬</span>
              <div>
                <span className="text-slate-600 dark:text-slate-400">備考:</span>
                <span className="ml-1 text-slate-700 dark:text-slate-300">
                  {hostPlant.notes}
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

/**
 * 観察タイプ別の優先度を取得（数値が小さいほど優先度が高い）
 */
const getObservationTypePriority = (observationType) => {
  switch (observationType) {
    case '野外（国内）': return 1; // 最優先
    case '飼育': return 2;
    case '野外（海外）':
    case '海外': return 3;
    default: return 4; // その他は最後
  }
};

/**
 * 統合食草情報表示コンポーネント
 */
const EnhancedHostPlantDisplay = ({ 
  hostPlants = [], 
  hostPlantsDetailed = [], 
  showDetailsByDefault = false,
  maxDisplayCount = 5 
}) => {
  const [expandedItems, setExpandedItems] = useState(new Set());
  const [showAll, setShowAll] = useState(false);
  
  // 詳細情報がある場合はそれを優先、なければ従来形式を使用
  let plantsToDisplay = hostPlantsDetailed && hostPlantsDetailed.length > 0 
    ? hostPlantsDetailed 
    : hostPlants.map(plant => ({
        name: typeof plant === 'string' ? plant.replace(/（.*）$/, '') : plant.name || plant,
        family: typeof plant === 'string' ? extractFamily(plant) : plant.family || '',
        displayName: typeof plant === 'string' ? plant : plant.displayName || plant.name || plant,
        observationType: '野外（国内）',
        plantPart: '葉',
        lifeStage: '幼虫',
        reference: '',
        notes: '',
        isDetailed: false
      }));

  // 「野外（国内）」を優先してソート
  plantsToDisplay = plantsToDisplay.sort((a, b) => {
    const priorityA = getObservationTypePriority(a.observationType);
    const priorityB = getObservationTypePriority(b.observationType);
    
    // 優先度が同じ場合は植物名でソート
    if (priorityA === priorityB) {
      return (a.name || '').localeCompare(b.name || '', 'ja');
    }
    
    return priorityA - priorityB;
  });
  
  const toggleExpanded = (index) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedItems(newExpanded);
  };
  
  if (!plantsToDisplay || plantsToDisplay.length === 0) {
    return (
      <div className="text-sm text-slate-500 dark:text-slate-400 italic">
        食草情報なし
      </div>
    );
  }
  
  const displayCount = showAll ? plantsToDisplay.length : Math.min(maxDisplayCount, plantsToDisplay.length);
  const hasMore = plantsToDisplay.length > maxDisplayCount;
  
  return (
    <div className="space-y-3">
      {/* 食草リスト */}
      <div className="space-y-2">
        {plantsToDisplay.slice(0, displayCount).map((hostPlant, index) => (
          <HostPlantDetailCard
            key={index}
            hostPlant={hostPlant}
            isExpanded={expandedItems.has(index) || showDetailsByDefault}
            onToggle={() => toggleExpanded(index)}
          />
        ))}
      </div>
      
      {/* "もっと見る" ボタン */}
      {hasMore && (
        <div className="text-center">
          <button
            onClick={() => setShowAll(!showAll)}
            className="inline-flex items-center px-3 py-2 text-sm font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 rounded-lg transition-colors"
          >
            {showAll ? '簡略表示' : `他${plantsToDisplay.length - maxDisplayCount}種を表示`}
            <svg 
              className={`ml-1 w-4 h-4 transition-transform ${showAll ? 'rotate-180' : ''}`}
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>
      )}
      
      {/* 統計情報 */}
      {plantsToDisplay.length > 1 && (
        <div className="text-xs text-slate-500 dark:text-slate-400 text-center pt-2 border-t border-slate-200 dark:border-slate-700">
          合計 {plantsToDisplay.length} 種の食草
          {hostPlantsDetailed && hostPlantsDetailed.length > 0 && (
            <span className="ml-2 text-emerald-600 dark:text-emerald-400">詳細情報あり</span>
          )}
        </div>
      )}
    </div>
  );
};

/**
 * 科名を抽出するヘルパー関数
 */
const extractFamily = (plantText) => {
  const match = plantText.match(/（([^）]+科)）/);
  return match ? match[1] : '';
};

export default EnhancedHostPlantDisplay;