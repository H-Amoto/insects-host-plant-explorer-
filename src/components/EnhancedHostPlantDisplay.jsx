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
    case '新芽': return '🌿';
    case '落果': return '🍎';
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
 * 植物記録をグループ化する関数
 */
const groupPlantsByName = (plants) => {
  const groups = {};
  
  plants.forEach(plant => {
    const key = plant.name;
    if (!groups[key]) {
      groups[key] = {
        name: plant.name,
        family: plant.family || '',
        records: []
      };
    }
    groups[key].records.push({
      observationType: plant.observationType,
      plantPart: plant.plantPart,
      lifeStage: plant.lifeStage,
      reference: plant.reference,
      notes: plant.notes
    });
  });
  
  return Object.values(groups);
};

/**
 * 個別食草情報の詳細表示コンポーネント（統合版）
 */
const HostPlantDetailCard = ({ plantGroup, isExpanded, onToggle }) => {
  // 最優先の観察タイプを決定（野外（国内）を最優先）
  const primaryRecord = plantGroup.records.reduce((prev, current) => {
    const prevPriority = getObservationTypePriority(prev.observationType);
    const currentPriority = getObservationTypePriority(current.observationType);
    return currentPriority < prevPriority ? current : prev;
  });
  
  const obsStyle = getObservationTypeStyle(primaryRecord.observationType);
  const isDomesticWild = primaryRecord.observationType === '野外（国内）';
  const cardOpacity = isDomesticWild ? 'opacity-100' : 'opacity-75';
  const cardFilter = isDomesticWild ? '' : 'saturate-75';
  
  // 利用情報をグループ化
  const usageInfo = plantGroup.records.reduce((acc, record) => {
    const key = `${record.lifeStage || ''}|${record.plantPart || ''}`;
    if (!acc[key]) {
      acc[key] = {
        lifeStage: record.lifeStage,
        plantPart: record.plantPart,
        observationTypes: new Set(),
        references: new Set(),
        notes: new Set()
      };
    }
    if (record.observationType) acc[key].observationTypes.add(record.observationType);
    if (record.reference) acc[key].references.add(record.reference);
    if (record.notes) acc[key].notes.add(record.notes);
    return acc;
  }, {});
  
  const usageInfoArray = Object.values(usageInfo);
  const hasMultipleUsages = usageInfoArray.length > 1;
  
  return (
    <div className={`rounded-lg border ${obsStyle.borderColor} ${obsStyle.bgColor} p-3 transition-all duration-200 ${cardOpacity} ${cardFilter}`}>
      {/* 基本情報行 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2 flex-1 min-w-0">
          <span className="text-lg">{obsStyle.icon}</span>
          <div className="flex-1 min-w-0">
            <span className={`font-medium ${isDomesticWild ? 'text-slate-800 dark:text-slate-200' : 'text-slate-600 dark:text-slate-400'}`}>
              {plantGroup.name}
            </span>
            {plantGroup.family && (
              <span className={`text-sm ml-1 ${isDomesticWild ? 'text-slate-600 dark:text-slate-400' : 'text-slate-500 dark:text-slate-500'}`}>
                （{plantGroup.family}）
              </span>
            )}
          </div>
          
          <span className={`text-xs px-2 py-1 rounded-full ${obsStyle.bgColor} ${obsStyle.textColor} font-medium`}>
            {obsStyle.label}
          </span>
        </div>
        
        {/* 詳細情報がある場合のトグルボタン - 複数利用がある場合のみ表示 */}
        {hasMultipleUsages && (
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
      
      {/* 単一利用の場合は直接詳細を表示 */}
      {!hasMultipleUsages && usageInfoArray.length > 0 && (
        <div className="mt-2 flex items-center space-x-4 text-sm text-slate-600 dark:text-slate-400">
          {usageInfoArray[0].lifeStage && (
            <div className="flex items-center space-x-1">
              <span>{getLifeStageIcon(usageInfoArray[0].lifeStage)}</span>
              <span>{usageInfoArray[0].lifeStage}</span>
            </div>
          )}
          {usageInfoArray[0].plantPart && (
            <div className="flex items-center space-x-1">
              <span>{getPlantPartIcon(usageInfoArray[0].plantPart)}</span>
              <span>{usageInfoArray[0].plantPart}</span>
            </div>
          )}
        </div>
      )}
      
      {/* 複数利用の詳細情報（常に表示） */}
      {hasMultipleUsages && (
        <div className="mt-3 pt-3 border-t border-slate-200 dark:border-slate-600 space-y-2">
          <div className="space-y-2">
            {usageInfoArray.map((usage, index) => (
              <div key={index} className="bg-slate-50 dark:bg-slate-800/50 rounded-md p-2 text-sm">
                <div className="flex items-center space-x-4">
                  {usage.lifeStage && (
                    <div className="flex items-center space-x-1">
                      <span>{getLifeStageIcon(usage.lifeStage)}</span>
                      <span className="text-slate-600 dark:text-slate-400">段階:</span>
                      <span className="font-medium">{usage.lifeStage}</span>
                    </div>
                  )}
                  {usage.plantPart && (
                    <div className="flex items-center space-x-1">
                      <span>{getPlantPartIcon(usage.plantPart)}</span>
                      <span className="text-slate-600 dark:text-slate-400">部位:</span>
                      <span className="font-medium">{usage.plantPart}</span>
                    </div>
                  )}
                </div>
                
                {/* 観察タイプ */}
                {usage.observationTypes.size > 0 && (
                  <div className="mt-1 flex items-center space-x-1">
                    <span className="text-slate-600 dark:text-slate-400">記録:</span>
                    <div className="flex flex-wrap gap-1">
                      {Array.from(usage.observationTypes).map(obsType => {
                        const style = getObservationTypeStyle(obsType);
                        return (
                          <span key={obsType} className={`text-xs px-1.5 py-0.5 rounded ${style.bgColor} ${style.textColor}`}>
                            {style.label}
                          </span>
                        );
                      })}
                    </div>
                  </div>
                )}
                
                {/* 参考文献 */}
                {usage.references.size > 0 && (
                  <div className="mt-1 flex items-center space-x-1">
                    <span className="text-slate-600 dark:text-slate-400">出典:</span>
                    <span className="text-slate-700 dark:text-slate-300">
                      {Array.from(usage.references).join(', ')}
                    </span>
                  </div>
                )}
                
                {/* 備考 */}
                {usage.notes.size > 0 && (
                  <div className="mt-1">
                    <span className="text-slate-600 dark:text-slate-400">備考:</span>
                    <div className="mt-1">
                      {Array.from(usage.notes).map(note => (
                        <div key={note} className="text-slate-700 dark:text-slate-300 text-xs">
                          {note}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
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

  // 同じ植物名の記録をグループ化
  const groupedPlants = groupPlantsByName(plantsToDisplay);

  // グループを「野外（国内）」を優先してソート
  const sortedGroups = groupedPlants.sort((a, b) => {
    // 各グループの最優先観察タイプを取得
    const priorityA = Math.min(...a.records.map(r => getObservationTypePriority(r.observationType)));
    const priorityB = Math.min(...b.records.map(r => getObservationTypePriority(r.observationType)));
    
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
  
  const displayCount = showAll ? sortedGroups.length : Math.min(maxDisplayCount, sortedGroups.length);
  const hasMore = sortedGroups.length > maxDisplayCount;
  
  return (
    <div className="space-y-3">
      {/* 食草リスト */}
      <div className="space-y-2">
        {sortedGroups.slice(0, displayCount).map((plantGroup, index) => (
          <HostPlantDetailCard
            key={`${plantGroup.name}-${index}`}
            plantGroup={plantGroup}
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
            {showAll ? '簡略表示' : `他${sortedGroups.length - maxDisplayCount}種を表示`}
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
      {sortedGroups.length > 1 && (
        <div className="text-xs text-slate-500 dark:text-slate-400 text-center pt-2 border-t border-slate-200 dark:border-slate-700">
          合計 {sortedGroups.length} 種の食草
          {(() => {
            const totalRecords = sortedGroups.reduce((sum, group) => sum + group.records.length, 0);
            return totalRecords > sortedGroups.length && (
              <span className="ml-2 text-slate-400 dark:text-slate-500">({totalRecords} 件の記録)</span>
            );
          })()} 
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