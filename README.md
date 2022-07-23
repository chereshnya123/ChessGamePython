# ChessGamePython
Обычные шахматы без графического интерфейса. Вся игра происходит в консоли, в которой выводится размеченное игровое поле 8х8. 
Вся игра происходит в консоли, взаимодействие с ней описывает во время игры, при запуске. 
Игра сыровата. Предполагается, что участники знают правила игры и не действуют вопреки им, иначе возможны ошибки и вылеты игры.
Также участники должны помнить свои фигуры и фигуры противника на поле, т.к. в консоли они отображаются одним цветом.
Обозначения фигур:
P (Pawn) - Пешка
R (Rook) - Ладья
K (Knight) - Конь
B (Bishop) - Слон
Q (Queen) - Ферзь
Значок короны - Король
Если фигура отображается на игровом поле маленькой буквой вместо заглавной, то это означает, что она может быть съедена другой фигурой, которую выбрал один из игроков.

Вся игра написана одним python-файлом с применением ООП (более 80% строк кода - описание методов и классов) без привлечения сторонних библиотек. 
На ранних этапах разработки игра дробилась на несколько файлов, однако в последствии они были объединены в один и удалены.

Интерфейс взаимодействия игроков с игрой находится в доработке
