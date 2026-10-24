from assistant.rules import reply, load_offices


def test_greeting():
    assert "Hello" in reply("hi")


def test_office_lookup():
    assert "I.101" in reply("Where is the Training Office?")


def test_unknown():
    assert "don't know" in reply("what is the meaning of life")


def test_empty():
    assert reply("   ") == "Please type a question."


def test_health_center_lookup():
    assert "A.105" in reply("Where is the Health Center?")


def test_international_office_lookup():
    assert "F.203" in reply("When does the International Office open?")



def test_help():
    """Check that the help command handles common input variations."""
    assert "I can help you find offices" in reply("help")
    assert "where is the library?" in reply("Help")

    # Case-insensitive input
    assert "I can help you find offices" in reply("HELP")

    # Leading and trailing whitespace
    assert "I can help you find offices" in reply("  help  ")

    # Trailing punctuation
    assert "I can help you find offices" in reply("help?!")



def test_greeting_good_morning():
    assert "Hello" in reply("good morning")
    assert "Hello" in reply("Good Morning!")


def test_greeting_case_insensitive():
    """Check greetings with mixed case and extra spaces."""
    assert "Hello" in reply("HI")
    assert "Hello" in reply("HeLLo")
    assert "Hello" in reply("   hi   ")


def test_office_lookup_case_insensitive():
    """Check office lookup with uppercase input."""
    result = reply("WHERE IS THE LIBRARY?")
    assert "Library" in result
    assert "B.201" in result
    assert "Mon-Sat 07:00-20:00" in result


def test_office_lookup_with_punctuation():
    """Check office lookup with trailing punctuation."""
    result = reply("Where is Student Affairs?!")
    assert "Student Affairs" in result
    assert "I.102" in result


def test_load_offices_csv():
    """Check that office information loads correctly from CSV."""
    offices = load_offices()

    assert "training office" in offices
    assert offices["training office"]["room"] == "I.101"
    assert offices["training office"]["hours"] == "Mon-Fri 07:30-16:30"


def test_office_csv_required_fields():
    """Check that all office records contain required information."""
    offices = load_offices()

    assert len(offices) > 0

    for name, office in offices.items():
        assert name == office["name"].lower()
        assert office["room"].strip()
        assert office["hours"].strip()
def test_new_offices_lookup():
    from assistant.rules import reply
    
    assert "A.02" in reply("where is testing & quality assurance?")
    assert "B.03" in reply("where is postgraduate studies?")
    assert "B.04" in reply("where is youth union office?")
    assert "H.101" in reply("where is dormitory management office?")
    assert "E.102" in reply("where is center for it application?")
    assert "A.103" in reply("where is educational testing office?")

    


def test_partial_name_training():
    """Check that typing 'training' finds 'Training Office'."""
    result = reply("training")
    assert "Training Office" in result
    assert "I.101" in result


def test_partial_name_in_question():
    """Check that partial office names work inside questions or for other offices."""
    result_training = reply("Where is training?")
    assert "Training Office" in result_training
    assert "I.101" in result_training

    result_health = reply("health")
    assert "Health Center" in result_health
    assert "A.105" in result_health

