def test_select(to_file, input_model_name, loss, ppl, time):
    with open(to_file, 'a') as file:
        file.write(f'{input_model_name};{loss};{ppl};{time}\n')


if __name__ == '__main__':
    test_select('a.csv', 'model1', 1, 10, 0.1)
    test_select('a.csv', 'model1-finetuned', 0.9, 9, 0.9)
    test_select('b.csv', 'model2', 1.5, 15, 0.2)
    test_select('b.csv', 'model2-finetuned', 0.9, 9, 0.1)
    # model1-finetuned score: -0.25
    # model2-finetuned score: 0.80
