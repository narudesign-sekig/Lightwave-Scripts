@script modeler
@version 2.6
@name "SelNextFGLayerPE"

//=======================================================
// SK_SelNextFGLayerPE.ls
//
// revision	: 1.00
// date		: 2016-09-15
// author	: naru design [ http://narudesign.com ]
//=======================================================

main
{
	// get foreground and background layer
	
	backgroundLayer = lyrbg();
	foregroundLayer = lyrfg();
	dataLayer = lyrdata();
	dataLayer.sortA();
	
	// 前景レイヤーが１つだけ選択されていない場合は終了
	if (foregroundLayer.size() != 1) {
		error("Invalid layer selection. Select one fg layer.");
		return;
	}
	
	//選択されている前景レイヤーを取得
	fg = foregroundLayer[1];
	
	// 全てのレイヤーを走査(小さいレイヤーから)
	for (i = 1; i <= dataLayer.size(); i++)
	{
		if (fg < dataLayer[i])
		{
			if (!isBackgroundLayer(dataLayer[i], backgroundLayer))
			{
				fg = dataLayer[i];
				lyrsetfg(fg);
				lyrsetbg(backgroundLayer);
				break;
			}
		}
	}
}

// 指定したレイヤーが、選択中の背景レイヤーか確認
isBackgroundLayer: lay, blay
{
	for (i = 1; i <= blay.size(); i++)
	{
		if (lay == blay[i]) return(true);
	}
	return(false);
}
