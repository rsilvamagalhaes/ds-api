## Console para Datastore do Google App Engine
> ferramenta com intuito de ajudar na manipulação do datastore do GAE, dado
> que o Datastore Viewer não é muito fácil de usar

### Como consultar
 - new ds.Query('User')
 - new ds.Query('User').limit(10)

 - new ds.Key('Kind', id)
 - new ds.Key('Kind', name)

#### Filtros 
1. EQUAL
 1.1 new ds.Query('User').eq('campo','valor')

2. IN 
 2.1 new ds.Query('User').inEq('campo','valor')

3. ORDER
 3.1 new ds.Query('User').order(*'campo1', 'campo2'*)
 3.2 new ds.Query('User').orderDesc(*'campo1', 'campo2'*)

4. NOT EQUAL
 4.1 new ds.Query('User').neq('campo', 'valor')

5. GT 
 5.1 new ds.Query('User').gt('campo', 'valor')

6. GTE
 6.1 new ds.Query('User').gte('campo', 'valor')

7. LT
 7.1 new ds.Query('User').lt('campo', 'valor')

8. LTE
 8.1 new ds.Query('User').lte('campo', 'valor')

### Como usar na sua aplicação
> git clone 

#### Abra o arquivo app.yaml, localizado na raiz do projeto
1. Edite o valor do *aplication* para o id da sua aplicação

#### Faça upload
> appcfg.py update .
*caso haja 2-steps-auth execute:*
> appcfg.py --oauth2  update .

#### Segurança
##### Por padrão somente usuários com a role de admin poderão acessar a url
> http://versao.seuapp.appspot.com/adm 

##### Para que outros usuarios tenham acesso à ferramenta, acesse o Datastore Admin no painel do Google App Engine

