from django.shortcuts import render
from setup.forms import SetupForm, MethodForm, RandomForm, RepeatForm, JadouNums, OptionalForm
from django.http import HttpResponse
from time import sleep
import os

#ファイル書き込み関数
def listwritedown(request, path, *arg):
	f = open(path, 'a')
	for l in arg:
		if request.POST[l] != '':
			if l == 'rsymmetry':
				w = request.POST[l]
				f.write('symmetry='+w+'\n')
			else:
				w = request.POST[l]
				f.write(l+'='+w+'\n')

def jadouwritedown(request, path, jpath):
		jnums = request.POST.getlist('jnums')
		#jnumsの数
		jnumsc = len(jnums)
		alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','Aa','Ab','Ac','Ad','Ae','Af','Ag','Ah','Ai','Aj','Ak','Al','Am','An','Ao','Ap','Aq','Ar','As','At','Au','Av','Aw','Ax','Ay','Az','Aa','Ab','Ac','Ad','Ae','Af','Ag','Ah','Ai','Aj','Ak','Al','Am','An','Ao','Ap','Aq','Ar','As','At','Au','Av','Aw','Ax','Ay','Az']
		filelist = []
		i = 0
		#子プロパティ作成
		for l in jnums:
			i += 1
			#現在の配列が最後から２番目ではない場合
			if i+1 < len(jnums):
				l = int(l)
				m = l+1
				for x in range(m):
					#最初
					if x == 0:
						for y in range(l):
							w = alpha[x]
							w += alpha[y]
							filelist.append(w)
					#２巡目以降
					else:
						n = int(jnums[i])
						for y in range(n):
							w = alpha[x]
							w += alpha[y]
							filelist.append(w)
			#配列が２個しかなかった場合
			elif len(jnums) == 2 and i == 1:
				l = int(l)
				for x in range(l):
					w = alpha[x]
					filelist.append(w)
#		for l in filelist:
#			print(l)
		#親プロパティマッチタイル書き込み
		#ループカウンタ
		loc = 0
		for l in filelist:
			#リストカウンタが最初の数より小さい時
			if loc < int(jnums[0]):
				f = open(path, 'a')
				w = 'tiles='
				l = int(jnums[0])
				#最初の数の分だけ書き込み
				for z in range(l):
					w += filelist[z]+' '
					loc += 1
				f.write(w+'\n'+'width='+jnums[0]+'\n'+'height=1')
			#子プロパティ作成
			elif loc < 8:
				#children counter
				ccount = 1
				#現在処理しているのがjnumsの最終項か（最終なら子はいらない）
				if 2 < len(jnums):
					for x in range(int(jnums[0])):
						mtpath = jpath+'mt'+str(ccount)+'.properties'
						ccount += 1
						f = open(mtpath, 'w')
						f.write('method=repeat\ntiles=')
						#1番目の入力値分繰り返し
						for m in range(int(jnums[1])):
							f.write(filelist[loc]+' ')
							loc += 1
						f.write('\nwidth='+jnums[1]+'\nheight=1\nmatchtiles=./'+filelist[x]+'.png')
		#孫プロパティ作成＠死にそう
		temp = []
		#最終項を除いた分の積
		times = 1
		for l in range(jnumsc-1):
			times = times * int(jnums[l])
		#掛ける数が2以下の場合
		if len(jnums) <= 2:
			for l in range(int(jnums[0])):
				temp.append(alpha[l])
		#掛ける数が3以上
		else:
			tmpcnt = 1
			for l in range(times):
				if tmpcnt < int(jnums[0]):
					temp.append(alpha[tmpcnt])
					tmpcnt += 1
				else:
					temp.append(alpha[tmpcnt])
					tmpcnt = 1
			tmpcnt = 0
			for l in range(len(temp)):
				t = temp[l]
				if tmpcnt+1 < int(jnums[1]):
					t += alpha[tmpcnt]
					temp[l] = t
					tmpcnt += 1
				else:
					t += alpha[tmpcnt]
					temp[l] = t
					tmpcnt = 0

		#一時配列
		templnums = []
		#最終項以外の積*最終項分の配列を作成、一時配列に順番に番号を入れる
		for m in range(times*int(jnums[jnumsc-1])):
			templnums.append(m)
		#親配列
		parearr = []
		for m in range(int(jnums[jnumsc-1])):
			for n in range(times):
				parearr.append(n)
		#子配列
		childarr = []
		for m in range(times):
			for n in range(int(jnums[jnumsc-1])):
				childarr.append(n)
		#ループのカウント
		lcount = 0
		pcount = 0
		chcount = 0
		for l in temp:
			#最終書き込みナンバー
			lnums = []
			mtpath = jpath+'mt'+str(ccount)+'.properties'
			ccount += 1
			f = open(mtpath, 'w')
			f.write('method=repeat\ntiles=')
			#一時配列から最終項分抜き出し処理
			#親配列から指定番号インデックス抜き出し
			parematch = [i for i, x in enumerate(parearr) if x == pcount]
			for m in parematch:
				#子配列から指定番号インデックス抜き出し
				childmatch = [i for i, x in enumerate(childarr) if x == chcount]
				#共通項を検索
				for m in parematch:
					if m in childmatch == True:
						lnums.append(templnums[childmatch.index(m)])
						chcount += 1
						break
			print(parematch)
			print(childmatch)


			#リスト書き出し
			for m in lnums:
				f.write(str(m)+' ')
			f.write('\nwidth='+jnums[jnumsc-1]+'\nheight=1\nmatchtiles=./'+l+'.png')
			lcount -= int(jnums[jnumsc-1])

#オプション項目書き込み関数　それぞれの項目に値が存在したときのみ書き込み
def optwritedown(request, path, *arg):
	f = open(path, 'a')
	for l in arg:
		if request.POST[l] != '':
			w = request.POST[l]
			f.write(l+'='+w+'\n')

#画面描画とPOST時の処理
def rendform(request):
	#POST時
	if request.method == 'POST':
		#独立したナンバリング作業用フォルダ作成
		n = 0
		e = True
		#ナンバリングフォルダの存在=Falseになるまでナンバーを+1して試行、Falseになったら作成
		while e == True:
			d = str(n)
			e = os.path.exists('generated/'+d)
			n+=1
		os.makedirs('generated/'+d)

		#ファイル作成
		w = request.POST['file_name']
		#ファイルネームを決定し、ファイルパスを指定
		path = 'generated/'+d+'/'+w+'.properties'
		jpath = 'generated/'+d+'/'
		f = open(path, 'w')

		#ファイルにフォームデータ書き込み
		listwritedown(request, path, 'tiles', 'method')

		#methodがrandomとrepeatの時に応じた書き込み　一致しない時は無視
		if request.POST['method'] == 'random':
			listwritedown(request, path, 'weight', 'linked', 'symmetry')
		elif request.POST['method'] == 'repeat':
			listwritedown(request, path, 'width', 'height', 'rsymmetry')
			if request.POST['jnums'] != '':
				jadouwritedown(request, path, jpath)

		#オプション項目書き込み
		optwritedown(request, path, 'source', 'metadata', 'faces', 'matchtiles', 'biomes', 'minheight', 'maxheight', 'matchblocks', 'connect', 'renderpass')
		#ファイルを閉じる
		f.close()

		#更新後にダイアログが出るようにする（頭いい方法募集）
		sleep(0.1)
		#作成したファイルをHttpResponseで返してダウンロードダイアログを表示させる
		response = HttpResponse(open(path,'rb').read(), content_type='application/properties')
		response['Content-Disposition'] = 'filename="%s.properties"' % w
		return response
	#それ以外はフォームをレンダリング
	else:
		return render(request, 'setup/form.html', {'setup': SetupForm(), 'method': MethodForm(), 'random': RandomForm(), 'repeat': RepeatForm(), 'jadou': JadouNums(), 'optional': OptionalForm()})