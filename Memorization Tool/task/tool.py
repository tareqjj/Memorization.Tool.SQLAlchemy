# write your code here
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box_num = Column(Integer, default=1)


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def main_menu():
    while True:
        print("1. Add flashcards")
        print("2. Practice flashcards")
        print("3. Exit")
        user_input = input()
        if user_input == "1":
            sub_menu()
            break
        elif user_input == "2":
            practice()
            break
        elif user_input == "3":
            exit_flash()
            break
        else:
            print(user_input, "is not an option")


def sub_menu():
    while True:
        print("1. Add a new flashcard")
        print("2. Exit")
        user_input = input()
        if user_input == "1":
            add_flashcard()
            break
        elif user_input == "2":
            session.commit()
            main_menu()
            break
        else:
            print(user_input, "is not an option")


def add_flashcard():
    while True:
        print("Question:")
        question_input = input().strip()
        if question_input != "":
            break
    while True:
        print("Answer:")
        answer_input = input().strip()
        if answer_input != "":
            break
    question_answer_pair = Flashcard(question=question_input, answer=answer_input)
    session.add(question_answer_pair)
    sub_menu()


def practice():
    flashcard_list = session.query(Flashcard).all()
    if flashcard_list:
        for card in flashcard_list:
            print("Question:", card.question)
            print('press "y" to see the answer:')
            print('press "n" to skip:')
            print('press "u" to update:')
            user_input = input()
            if user_input == "y":
                print("Answer:", card.answer)
                learning_menu(card)
                continue
            elif user_input == "n":
                continue
            elif user_input == "u":
                update_flashcard(card)
                continue
            else:
                print(user_input, "is not an option")
        main_menu()
    else:
        print("There is no flashcard to practice!")
        main_menu()


def update_flashcard(card):
    while True:
        print('press "d" to delete the flashcard:')
        print('press "e" to edit the flashcard:')
        user_input = input()
        if user_input == "d":
            session.delete(card)
            session.commit()
            break
        elif user_input == "e":
            print(f"current question: {card.question}")
            print("please write a new question:")
            new_question = input().strip()
            if new_question:
                card.question = new_question
                session.commit()
            print(f"current answer: {card.answer}")
            print("please write a new answer:")
            new_answer = input().strip()
            if new_answer:
                card.answer = new_answer
                session.commit()
            break
        else:
            print(user_input, "is not an option")


def learning_menu(card):
    while True:
        print('press "y" if your answer is correct:')
        print('press "n" if your answer is wrong:')
        user_input = input()
        if user_input == "y":
            if card.box_num == 3:
                session.delete(card)
                session.commit()
            else:
                card.box_num += 1
                session.commit()
            break
        elif user_input == "n":
            if card.box_num > 1:
                card.box_num -= 1
                session.commit()
            break
        else:
            print(user_input, "is not an option")


def exit_flash():
    print("Bye!")


main_menu()
