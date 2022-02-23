## История версий

### Версия 1.1.0

#### **Package.json**

- замена пакетного менеджера **npm** на **yarn**
- замена **package.json.lock** на **yarn.lock**
- перенос зависимостей из продакшн в девелопмент
- добавлена поддержка **postcss**, **stylus**, **imagemin**
- добавлен линтер CSS **Stylelint**

Как следствие, запуск дев-сервера
`yarn dev `
или
`npm dev`

Сборка проекта
`yarn build`
или
`npm build`

Скрипты `npm sass` и `npm start` не нужны, в ближайщее время будут удалены

#### **Webpack**

- общий файл конфигурации разбит на три части: базовый, разработка (_dev_) и релиз (_prod_)
- изменена структура каталогов при запуске команды `yarn build`

      -build
        |
        |-assets
          |-fonts
          |-img
        |-css
        |-js
        |
        index.html
        manifest.json
        robots.txt

- добавлен алиас для каталога src. Теперь для задания пути файла не требуется использовать многослойные переходы
  `../../../path/to/resource`
  достаточно указать
  `~/path/to/resource`

#### **Файлы конфигурации**

Добавлен файл конфигурации **.editorconfig**
Добавлен файл конфигурации **.eslintrc**
Добавлен файл конфигурации **.stylelintrc.json**

## Полезная информация

**Сравнение пакетных менеджеров npm vs yarn**

https://www.youtube.com/watch?v=0DGClZD5LEM
https://www.youtube.com/watch?v=0DGClZD5LEM
https://prgssr.ru/development/yarn-ili-npm-vse-chto-vam-nuzhno-znat.html

**Документация по Stylus**

https://sass-lang.com/documentation

**О преимуществах Stylus**

https://habr.com/ru/company/yandex/blog/169415/

**Документация по SASS**

https://sass-lang.com/documentation

**Документация по PostCSS**

https://postcss.org/api/
