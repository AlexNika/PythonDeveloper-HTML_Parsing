import pickle

greetings = ['Я не видел тебя так давно, что, кажется, что забыл черты твоего лица! Привет!',
             'Ничего себе! Ты так изменился, а может, я просто давно тебя не видел! Привет!',
             'Готов поспорить, что ты не видел меня так же давно, как и я тебя! Привет!',
             'Привет! Ставлю тебе лайк, как поживаешь?',
             'Привет! Не верю своим глазам! А ну-ка, протри-ка мне стекла!',
             'Привет! Мне кажется, или я реально тебя вижу?',
             'Ну ничего себе какие люди нарисовались перед моими глазами! Привет!',
             'Мираж! Это точно мираж! Ну, не может быть, что я вижу тебя прямо перед собой! Здравствуй!',
             'О, здравствуй, мой драгоценный друг!',
             'А я-то думаю, что за свет впереди, а оказывается, это ты идешь по дороге! Приветствую!',
             'О том, что я увижу тебя мне подсказало внутреннее чувство. Да, я предчувствовал тебя сегодня! Привет!',
             'О! Привет! Я о тебе сегодня видел сюжет в новостях! Сказали, что я непременно тебя сегодня встречу!',
             'Здравствуйте, несказанно рад видеть вашу физиономию перед собой!',
             'Здравствуй! У меня, наверное, голова кругом идет или это и вправду ты?',
             'Привет! Ничего себе! Да сегодня дождь пошел только потому, что я тебя встретил!',
             'Самое необычное, что сегодня могло со мной произойти – это встреча с тобой! Привет!',
             'Здравствуй! Стоп! Стоп! Стоп! Дай я тебя сфотографирую, иначе никто не поверит, что я тебя видел!',
             'Да это просто праздник какой-то! Я встретил тебя здесь и без охраны! Привет!',
             'Привет! Какие люди! Рад вас видеть вот тут, просто так, как живого человека… я-то думал вы – призрак!',
             'Вот так вот вечность пропадал и вдруг … стоишь передо мной! Я в шоке! Привет!',
             'Приветушечки!',
             'Санни дэй, бро!',
             'Алло, товарищ!',
             'Действительно рад!',
             'Здравствуйте! Царь!',
             'Обалдеть, кто это?',
             'Чига буга!',
             'Здоровичики!',
             'Ку!',
             'Хай пипл!',
             'Ни хау!',
             'Салам!',
             'Дратути!',
             'Даров!',
             'Кукусики!',
             'Привет! С тебя лайк!',
             'Лайк тебе!',
             'Хаю Хай!']
filename = 'greetings.pkl'
with open(filename, 'wb') as f:
    pickle.dump(greetings, f)
    f.close()
