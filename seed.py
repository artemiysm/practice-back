from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.survey import Survey, Question, Option, SurveyStatus, QuestionType
from app.models.answer import Response, Answer
from datetime import datetime, timedelta, timezone


def create_test_data():
    """Создание тестовых данных"""
    
    print(" Начинаем создание тестовых данных...")
    
    with app.app_context():
        # Очищаем базу
        print("  Очистка существующих данных...")
        db.session.query(Answer).delete()
        db.session.query(Response).delete()
        db.session.query(Option).delete()
        db.session.query(Question).delete()
        db.session.query(Survey).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Создаем тестовых пользователей
        print(" Создаем пользователей...")
        
        user1 = User(email='author@example.com')
        user1.set_password('password123')
        db.session.add(user1)
        
        user2 = User(email='respondent@example.com')
        user2.set_password('password123')
        db.session.add(user2)
        
        user3 = User(email='test@example.com')
        user3.set_password('password123')
        db.session.add(user3)
        
        db.session.commit()
        print(f" Создано {User.query.count()} пользователей")
    
        # Создаем тестовые опросы
        print(" Создаем опросы...")
        
        # Опрос 1: Удовлетворенность клиентов
        survey1 = Survey(
            title='Удовлетворенность клиентов',
            description='Пожалуйста, ответьте на несколько вопросов о нашем сервисе',
            author_id=user1.id,
            status=SurveyStatus.PUBLISHED,
            created_at=datetime.now(timezone.utc) - timedelta(days=7)
        )
        db.session.add(survey1)
        db.session.flush()
        
        # Вопрос 1.1: Одиночный выбор
        q1_1 = Question(
            survey_id=survey1.id,
            text='Как вы оцениваете наш сервис?',
            q_type=QuestionType.SINGLE,
            order=1
        )
        db.session.add(q1_1)
        db.session.flush()
        
        # Варианты для вопроса 1.1
        options_1_1 = [
            Option(question_id=q1_1.id, text='Отлично'),
            Option(question_id=q1_1.id, text='Хорошо'),
            Option(question_id=q1_1.id, text='Удовлетворительно'),
            Option(question_id=q1_1.id, text='Плохо'),
        ]
        db.session.add_all(options_1_1)
        
        # Вопрос 1.2: Множественный выбор
        q1_2 = Question(
            survey_id=survey1.id,
            text='Что вам понравилось больше всего? (можно выбрать несколько)',
            q_type=QuestionType.MULTIPLE,
            order=2
        )
        db.session.add(q1_2)
        db.session.flush()
        
        # Варианты для вопроса 1.2
        options_1_2 = [
            Option(question_id=q1_2.id, text='Скорость работы'),
            Option(question_id=q1_2.id, text='Качество обслуживания'),
            Option(question_id=q1_2.id, text='Цена'),
            Option(question_id=q1_2.id, text='Ассортимент'),
        ]
        db.session.add_all(options_1_2)
        
        # Вопрос 1.3: Текстовый
        q1_3 = Question(
            survey_id=survey1.id,
            text='Ваши пожелания и комментарии',
            q_type=QuestionType.TEXT,
            order=3
        )
        db.session.add(q1_3)
        
        # Опрос 2: Черновик
        survey2 = Survey(
            title='Опрос о новых функциях (Черновик)',
            description='Этот опрос еще не опубликован',
            author_id=user1.id,
            status=SurveyStatus.DRAFT,
            created_at=datetime.now(timezone.utc) - timedelta(days=2)
        )
        db.session.add(survey2)
        db.session.flush()
        
        q2_1 = Question(
            survey_id=survey2.id,
            text='Какую функцию вы хотели бы видеть?',
            q_type=QuestionType.TEXT,
            order=1
        )
        db.session.add(q2_1)
        
        # Опрос 3: Закрытый
        survey3 = Survey(
            title='Опрос о продукте (Закрыт)',
            description='Этот опрос завершен',
            author_id=user1.id,
            status=SurveyStatus.CLOSED,
            created_at=datetime.now(timezone.utc) - timedelta(days=30)
        )
        db.session.add(survey3)
        db.session.flush()
        
        q3_1 = Question(
            survey_id=survey3.id,
            text='Вам нравится наш продукт?',
            q_type=QuestionType.SINGLE,
            order=1
        )
        db.session.add(q3_1)
        db.session.flush()
        
        options_3_1 = [
            Option(question_id=q3_1.id, text='Да'),
            Option(question_id=q3_1.id, text='Нет'),
        ]
        db.session.add_all(options_3_1)
        
        db.session.commit()
        print(f" Создано {Survey.query.count()} опросов")
        
        # Создаем тестовые ответы
        print(" Создаем ответы респондентов...")
        
        # Респондент 2 проходит опрос 1
        response1 = Response(
            survey_id=survey1.id,
            user_id=user2.id,
            submitted_at=datetime.now(timezone.utc) - timedelta(days=5)
        )
        db.session.add(response1)
        db.session.flush()
        
        # Ответы на вопросы
        ans1_1 = Answer(
            response_id=response1.id,
            question_id=q1_1.id,
            option_id=options_1_1[0].id  # Отлично
        )
        db.session.add(ans1_1)
        
        ans1_2 = Answer(
            response_id=response1.id,
            question_id=q1_2.id,
            option_id=options_1_2[0].id  # Скорость работы
        )
        db.session.add(ans1_2)
        
        ans1_3 = Answer(
            response_id=response1.id,
            question_id=q1_3.id,
            text_value='Отличный сервис, рекомендую!'
        )
        db.session.add(ans1_3)
        
        # Респондент 3 проходит опрос 1
        response2 = Response(
            survey_id=survey1.id,
            user_id=user3.id,
            submitted_at=datetime.now(timezone.utc) - timedelta(days=3)
        )
        db.session.add(response2)
        db.session.flush()
        
        ans2_1 = Answer(
            response_id=response2.id,
            question_id=q1_1.id,
            option_id=options_1_1[1].id  # Хорошо
        )
        db.session.add(ans2_1)
        
        ans2_2a = Answer(
            response_id=response2.id,
            question_id=q1_2.id,
            option_id=options_1_2[1].id  # Качество обслуживания
        )
        db.session.add(ans2_2a)
        
        ans2_2b = Answer(
            response_id=response2.id,
            question_id=q1_2.id,
            option_id=options_1_2[2].id  # Цена
        )
        db.session.add(ans2_2b)
        
        ans2_3 = Answer(
            response_id=response2.id,
            question_id=q1_3.id,
            text_value='Все хорошо, но можно улучшить поддержку'
        )
        db.session.add(ans2_3)
        
        db.session.commit()
        print(f" Создано {Response.query.count()} ответов")
        
        # Итоговая статистика
        
        print(" ИТОГОВАЯ СТАТИСТИКА:")
       
        print(f" Пользователей: {User.query.count()}")
        print(f" Опросов: {Survey.query.count()}")
        print(f"   - Опубликованных: {Survey.query.filter_by(status=SurveyStatus.PUBLISHED).count()}")
        print(f"   - Черновиков: {Survey.query.filter_by(status=SurveyStatus.DRAFT).count()}")
        print(f"   - Закрытых: {Survey.query.filter_by(status=SurveyStatus.CLOSED).count()}")
        print(f" Вопросов: {Question.query.count()}")
        print(f" Вариантов ответов: {Option.query.count()}")
        print(f" Прохождений опросов: {Response.query.count()}")
        print(f" Ответов на вопросы: {Answer.query.count()}")
        
        
        # Выводим данные для входа
        print("\n ДАННЫЕ ДЛЯ ВХОДА:")
        
        print("Автор (создает опросы):")
        print("  Email: author@example.com")
        print("  Password: password123")
        print("\nРеспондент 1:")
        print("  Email: respondent@example.com")
        print("  Password: password123")
        print("\nРеспондент 2:")
        print("  Email: test@example.com")
        print("  Password: password123")
        
        
        print("\nТестовые данные успешно созданы!")


if __name__ == '__main__':
    app = create_app()
    create_test_data()