// Generated from /Users/ivanleskin/PycharmProjects/ISERV/src/JavaEL_lex/JavaELLexer.g4 by ANTLR 4.9.1
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class JavaELLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.9.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		OpenParen=1, CloseParen=2, OpenBracket=3, CloseBracket=4, And=5, Or=6, 
		Not=7, Equality=8, Relation=9, Logical=10, Equal=11, NotEqual=12, Greater=13, 
		Less=14, GreaterEqual=15, LessEqual=16, Dot=17, Comma=18, Question=19, 
		DoubleDots=20, Plus=21, Minus=22, Mul=23, Div=24, Mod=25, Empty=26, BooleanLiteral=27, 
		NullLiteral=28, StringLiteral=29, IntegerLiteral=30, WS=31, Identifyer=32;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"OpenParen", "CloseParen", "OpenBracket", "CloseBracket", "And", "Or", 
			"Not", "Equality", "Relation", "Logical", "Equal", "NotEqual", "Greater", 
			"Less", "GreaterEqual", "LessEqual", "Dot", "Comma", "Question", "DoubleDots", 
			"Plus", "Minus", "Mul", "Div", "Mod", "Empty", "BooleanLiteral", "NullLiteral", 
			"StringLiteral", "IntegerLiteral", "WS", "Identifyer", "DecimalIntegerLiteral", 
			"DoubleStringCharacter", "SingleStringCharacter", "EscapeSequence", "CharacterEscapeSequence", 
			"HexEscapeSequence", "UnicodeEscapeSequence", "ExtendedUnicodeEscapeSequence", 
			"SingleEscapeCharacter", "NonEscapeCharacter", "EscapeCharacter", "LineContinuation", 
			"HexDigit"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'('", "')'", "'['", "']'", null, null, null, null, null, null, 
			null, null, null, null, null, null, "'.'", "','", "'?'", "':'", "'+'", 
			"'-'", "'*'", null, null, "'empty'", null, "'null'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "OpenParen", "CloseParen", "OpenBracket", "CloseBracket", "And", 
			"Or", "Not", "Equality", "Relation", "Logical", "Equal", "NotEqual", 
			"Greater", "Less", "GreaterEqual", "LessEqual", "Dot", "Comma", "Question", 
			"DoubleDots", "Plus", "Minus", "Mul", "Div", "Mod", "Empty", "BooleanLiteral", 
			"NullLiteral", "StringLiteral", "IntegerLiteral", "WS", "Identifyer"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public JavaELLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "JavaELLexer.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\"\u0152\b\1\4\2\t"+
		"\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4"+
		",\t,\4-\t-\4.\t.\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\6\3\6\3\6\5"+
		"\6k\n\6\3\7\3\7\3\7\3\7\5\7q\n\7\3\b\3\b\3\b\3\b\5\bw\n\b\3\t\3\t\5\t"+
		"{\n\t\3\n\3\n\3\n\3\n\5\n\u0081\n\n\3\13\3\13\3\13\5\13\u0086\n\13\3\f"+
		"\3\f\3\f\3\f\5\f\u008c\n\f\3\r\3\r\3\r\3\r\5\r\u0092\n\r\3\16\3\16\3\16"+
		"\5\16\u0097\n\16\3\17\3\17\3\17\5\17\u009c\n\17\3\20\3\20\3\20\3\20\5"+
		"\20\u00a2\n\20\3\21\3\21\3\21\3\21\5\21\u00a8\n\21\3\22\3\22\3\23\3\23"+
		"\3\24\3\24\3\25\3\25\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31\3\31\3\31"+
		"\5\31\u00bc\n\31\3\32\3\32\3\32\3\32\5\32\u00c2\n\32\3\33\3\33\3\33\3"+
		"\33\3\33\3\33\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\5\34\u00d3"+
		"\n\34\3\35\3\35\3\35\3\35\3\35\3\36\3\36\7\36\u00dc\n\36\f\36\16\36\u00df"+
		"\13\36\3\36\3\36\3\36\7\36\u00e4\n\36\f\36\16\36\u00e7\13\36\3\36\5\36"+
		"\u00ea\n\36\3\37\3\37\3 \6 \u00ef\n \r \16 \u00f0\3 \3 \3!\6!\u00f6\n"+
		"!\r!\16!\u00f7\3!\7!\u00fb\n!\f!\16!\u00fe\13!\3!\7!\u0101\n!\f!\16!\u0104"+
		"\13!\3\"\3\"\3\"\7\"\u0109\n\"\f\"\16\"\u010c\13\"\5\"\u010e\n\"\3#\3"+
		"#\3#\3#\5#\u0114\n#\3$\3$\3$\3$\5$\u011a\n$\3%\3%\3%\3%\3%\5%\u0121\n"+
		"%\3&\3&\5&\u0125\n&\3\'\3\'\3\'\3\'\3(\3(\3(\3(\3(\3(\3(\3(\3(\3(\6(\u0135"+
		"\n(\r(\16(\u0136\3(\3(\5(\u013b\n(\3)\3)\3)\6)\u0140\n)\r)\16)\u0141\3"+
		")\3)\3*\3*\3+\3+\3,\3,\5,\u014c\n,\3-\3-\3-\3.\3.\2\2/\3\3\5\4\7\5\t\6"+
		"\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24"+
		"\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C\2E\2G\2"+
		"I\2K\2M\2O\2Q\2S\2U\2W\2Y\2[\2\3\2\r\5\2\13\f\17\17\"\"\5\2C\\aac|\3\2"+
		"\63;\3\2\62;\6\2\f\f\17\17$$^^\6\2\f\f\17\17))^^\13\2$$))^^ddhhppttvv"+
		"xx\16\2\f\f\17\17$$))\62;^^ddhhppttvxzz\5\2\62;wwzz\5\2\f\f\17\17\u202a"+
		"\u202b\6\2\62;CHaach\2\u016c\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3"+
		"\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2"+
		"\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37"+
		"\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3"+
		"\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2"+
		"\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\3]"+
		"\3\2\2\2\5_\3\2\2\2\7a\3\2\2\2\tc\3\2\2\2\13j\3\2\2\2\rp\3\2\2\2\17v\3"+
		"\2\2\2\21z\3\2\2\2\23\u0080\3\2\2\2\25\u0085\3\2\2\2\27\u008b\3\2\2\2"+
		"\31\u0091\3\2\2\2\33\u0096\3\2\2\2\35\u009b\3\2\2\2\37\u00a1\3\2\2\2!"+
		"\u00a7\3\2\2\2#\u00a9\3\2\2\2%\u00ab\3\2\2\2\'\u00ad\3\2\2\2)\u00af\3"+
		"\2\2\2+\u00b1\3\2\2\2-\u00b3\3\2\2\2/\u00b5\3\2\2\2\61\u00bb\3\2\2\2\63"+
		"\u00c1\3\2\2\2\65\u00c3\3\2\2\2\67\u00d2\3\2\2\29\u00d4\3\2\2\2;\u00e9"+
		"\3\2\2\2=\u00eb\3\2\2\2?\u00ee\3\2\2\2A\u00f5\3\2\2\2C\u010d\3\2\2\2E"+
		"\u0113\3\2\2\2G\u0119\3\2\2\2I\u0120\3\2\2\2K\u0124\3\2\2\2M\u0126\3\2"+
		"\2\2O\u013a\3\2\2\2Q\u013c\3\2\2\2S\u0145\3\2\2\2U\u0147\3\2\2\2W\u014b"+
		"\3\2\2\2Y\u014d\3\2\2\2[\u0150\3\2\2\2]^\7*\2\2^\4\3\2\2\2_`\7+\2\2`\6"+
		"\3\2\2\2ab\7]\2\2b\b\3\2\2\2cd\7_\2\2d\n\3\2\2\2ef\7c\2\2fg\7p\2\2gk\7"+
		"f\2\2hi\7(\2\2ik\7(\2\2je\3\2\2\2jh\3\2\2\2k\f\3\2\2\2lm\7q\2\2mq\7t\2"+
		"\2no\7~\2\2oq\7~\2\2pl\3\2\2\2pn\3\2\2\2q\16\3\2\2\2rs\7p\2\2st\7q\2\2"+
		"tw\7v\2\2uw\7#\2\2vr\3\2\2\2vu\3\2\2\2w\20\3\2\2\2x{\5\27\f\2y{\5\31\r"+
		"\2zx\3\2\2\2zy\3\2\2\2{\22\3\2\2\2|\u0081\5\33\16\2}\u0081\5\35\17\2~"+
		"\u0081\5\37\20\2\177\u0081\5!\21\2\u0080|\3\2\2\2\u0080}\3\2\2\2\u0080"+
		"~\3\2\2\2\u0080\177\3\2\2\2\u0081\24\3\2\2\2\u0082\u0086\5\13\6\2\u0083"+
		"\u0086\5\r\7\2\u0084\u0086\5\17\b\2\u0085\u0082\3\2\2\2\u0085\u0083\3"+
		"\2\2\2\u0085\u0084\3\2\2\2\u0086\26\3\2\2\2\u0087\u0088\7?\2\2\u0088\u008c"+
		"\7?\2\2\u0089\u008a\7g\2\2\u008a\u008c\7s\2\2\u008b\u0087\3\2\2\2\u008b"+
		"\u0089\3\2\2\2\u008c\30\3\2\2\2\u008d\u008e\7#\2\2\u008e\u0092\7?\2\2"+
		"\u008f\u0090\7p\2\2\u0090\u0092\7g\2\2\u0091\u008d\3\2\2\2\u0091\u008f"+
		"\3\2\2\2\u0092\32\3\2\2\2\u0093\u0094\7i\2\2\u0094\u0097\7v\2\2\u0095"+
		"\u0097\7@\2\2\u0096\u0093\3\2\2\2\u0096\u0095\3\2\2\2\u0097\34\3\2\2\2"+
		"\u0098\u0099\7n\2\2\u0099\u009c\7v\2\2\u009a\u009c\7>\2\2\u009b\u0098"+
		"\3\2\2\2\u009b\u009a\3\2\2\2\u009c\36\3\2\2\2\u009d\u009e\7i\2\2\u009e"+
		"\u00a2\7g\2\2\u009f\u00a0\7@\2\2\u00a0\u00a2\7?\2\2\u00a1\u009d\3\2\2"+
		"\2\u00a1\u009f\3\2\2\2\u00a2 \3\2\2\2\u00a3\u00a4\7n\2\2\u00a4\u00a8\7"+
		"g\2\2\u00a5\u00a6\7>\2\2\u00a6\u00a8\7?\2\2\u00a7\u00a3\3\2\2\2\u00a7"+
		"\u00a5\3\2\2\2\u00a8\"\3\2\2\2\u00a9\u00aa\7\60\2\2\u00aa$\3\2\2\2\u00ab"+
		"\u00ac\7.\2\2\u00ac&\3\2\2\2\u00ad\u00ae\7A\2\2\u00ae(\3\2\2\2\u00af\u00b0"+
		"\7<\2\2\u00b0*\3\2\2\2\u00b1\u00b2\7-\2\2\u00b2,\3\2\2\2\u00b3\u00b4\7"+
		"/\2\2\u00b4.\3\2\2\2\u00b5\u00b6\7,\2\2\u00b6\60\3\2\2\2\u00b7\u00bc\7"+
		"\61\2\2\u00b8\u00b9\7f\2\2\u00b9\u00ba\7k\2\2\u00ba\u00bc\7x\2\2\u00bb"+
		"\u00b7\3\2\2\2\u00bb\u00b8\3\2\2\2\u00bc\62\3\2\2\2\u00bd\u00c2\7\'\2"+
		"\2\u00be\u00bf\7o\2\2\u00bf\u00c0\7q\2\2\u00c0\u00c2\7f\2\2\u00c1\u00bd"+
		"\3\2\2\2\u00c1\u00be\3\2\2\2\u00c2\64\3\2\2\2\u00c3\u00c4\7g\2\2\u00c4"+
		"\u00c5\7o\2\2\u00c5\u00c6\7r\2\2\u00c6\u00c7\7v\2\2\u00c7\u00c8\7{\2\2"+
		"\u00c8\66\3\2\2\2\u00c9\u00ca\7v\2\2\u00ca\u00cb\7t\2\2\u00cb\u00cc\7"+
		"w\2\2\u00cc\u00d3\7g\2\2\u00cd\u00ce\7h\2\2\u00ce\u00cf\7c\2\2\u00cf\u00d0"+
		"\7n\2\2\u00d0\u00d1\7u\2\2\u00d1\u00d3\7g\2\2\u00d2\u00c9\3\2\2\2\u00d2"+
		"\u00cd\3\2\2\2\u00d38\3\2\2\2\u00d4\u00d5\7p\2\2\u00d5\u00d6\7w\2\2\u00d6"+
		"\u00d7\7n\2\2\u00d7\u00d8\7n\2\2\u00d8:\3\2\2\2\u00d9\u00dd\7$\2\2\u00da"+
		"\u00dc\5E#\2\u00db\u00da\3\2\2\2\u00dc\u00df\3\2\2\2\u00dd\u00db\3\2\2"+
		"\2\u00dd\u00de\3\2\2\2\u00de\u00e0\3\2\2\2\u00df\u00dd\3\2\2\2\u00e0\u00ea"+
		"\7$\2\2\u00e1\u00e5\7)\2\2\u00e2\u00e4\5G$\2\u00e3\u00e2\3\2\2\2\u00e4"+
		"\u00e7\3\2\2\2\u00e5\u00e3\3\2\2\2\u00e5\u00e6\3\2\2\2\u00e6\u00e8\3\2"+
		"\2\2\u00e7\u00e5\3\2\2\2\u00e8\u00ea\7)\2\2\u00e9\u00d9\3\2\2\2\u00e9"+
		"\u00e1\3\2\2\2\u00ea<\3\2\2\2\u00eb\u00ec\5C\"\2\u00ec>\3\2\2\2\u00ed"+
		"\u00ef\t\2\2\2\u00ee\u00ed\3\2\2\2\u00ef\u00f0\3\2\2\2\u00f0\u00ee\3\2"+
		"\2\2\u00f0\u00f1\3\2\2\2\u00f1\u00f2\3\2\2\2\u00f2\u00f3\b \2\2\u00f3"+
		"@\3\2\2\2\u00f4\u00f6\t\3\2\2\u00f5\u00f4\3\2\2\2\u00f6\u00f7\3\2\2\2"+
		"\u00f7\u00f5\3\2\2\2\u00f7\u00f8\3\2\2\2\u00f8\u00fc\3\2\2\2\u00f9\u00fb"+
		"\5C\"\2\u00fa\u00f9\3\2\2\2\u00fb\u00fe\3\2\2\2\u00fc\u00fa\3\2\2\2\u00fc"+
		"\u00fd\3\2\2\2\u00fd\u0102\3\2\2\2\u00fe\u00fc\3\2\2\2\u00ff\u0101\t\3"+
		"\2\2\u0100\u00ff\3\2\2\2\u0101\u0104\3\2\2\2\u0102\u0100\3\2\2\2\u0102"+
		"\u0103\3\2\2\2\u0103B\3\2\2\2\u0104\u0102\3\2\2\2\u0105\u010e\7\62\2\2"+
		"\u0106\u010a\t\4\2\2\u0107\u0109\t\5\2\2\u0108\u0107\3\2\2\2\u0109\u010c"+
		"\3\2\2\2\u010a\u0108\3\2\2\2\u010a\u010b\3\2\2\2\u010b\u010e\3\2\2\2\u010c"+
		"\u010a\3\2\2\2\u010d\u0105\3\2\2\2\u010d\u0106\3\2\2\2\u010eD\3\2\2\2"+
		"\u010f\u0114\n\6\2\2\u0110\u0111\7^\2\2\u0111\u0114\5I%\2\u0112\u0114"+
		"\5Y-\2\u0113\u010f\3\2\2\2\u0113\u0110\3\2\2\2\u0113\u0112\3\2\2\2\u0114"+
		"F\3\2\2\2\u0115\u011a\n\7\2\2\u0116\u0117\7^\2\2\u0117\u011a\5I%\2\u0118"+
		"\u011a\5Y-\2\u0119\u0115\3\2\2\2\u0119\u0116\3\2\2\2\u0119\u0118\3\2\2"+
		"\2\u011aH\3\2\2\2\u011b\u0121\5K&\2\u011c\u0121\7\62\2\2\u011d\u0121\5"+
		"M\'\2\u011e\u0121\5O(\2\u011f\u0121\5Q)\2\u0120\u011b\3\2\2\2\u0120\u011c"+
		"\3\2\2\2\u0120\u011d\3\2\2\2\u0120\u011e\3\2\2\2\u0120\u011f\3\2\2\2\u0121"+
		"J\3\2\2\2\u0122\u0125\5S*\2\u0123\u0125\5U+\2\u0124\u0122\3\2\2\2\u0124"+
		"\u0123\3\2\2\2\u0125L\3\2\2\2\u0126\u0127\7z\2\2\u0127\u0128\5[.\2\u0128"+
		"\u0129\5[.\2\u0129N\3\2\2\2\u012a\u012b\7w\2\2\u012b\u012c\5[.\2\u012c"+
		"\u012d\5[.\2\u012d\u012e\5[.\2\u012e\u012f\5[.\2\u012f\u013b\3\2\2\2\u0130"+
		"\u0131\7w\2\2\u0131\u0132\7}\2\2\u0132\u0134\5[.\2\u0133\u0135\5[.\2\u0134"+
		"\u0133\3\2\2\2\u0135\u0136\3\2\2\2\u0136\u0134\3\2\2\2\u0136\u0137\3\2"+
		"\2\2\u0137\u0138\3\2\2\2\u0138\u0139\7\177\2\2\u0139\u013b\3\2\2\2\u013a"+
		"\u012a\3\2\2\2\u013a\u0130\3\2\2\2\u013bP\3\2\2\2\u013c\u013d\7w\2\2\u013d"+
		"\u013f\7}\2\2\u013e\u0140\5[.\2\u013f\u013e\3\2\2\2\u0140\u0141\3\2\2"+
		"\2\u0141\u013f\3\2\2\2\u0141\u0142\3\2\2\2\u0142\u0143\3\2\2\2\u0143\u0144"+
		"\7\177\2\2\u0144R\3\2\2\2\u0145\u0146\t\b\2\2\u0146T\3\2\2\2\u0147\u0148"+
		"\n\t\2\2\u0148V\3\2\2\2\u0149\u014c\5S*\2\u014a\u014c\t\n\2\2\u014b\u0149"+
		"\3\2\2\2\u014b\u014a\3\2\2\2\u014cX\3\2\2\2\u014d\u014e\7^\2\2\u014e\u014f"+
		"\t\13\2\2\u014fZ\3\2\2\2\u0150\u0151\t\f\2\2\u0151\\\3\2\2\2#\2jpvz\u0080"+
		"\u0085\u008b\u0091\u0096\u009b\u00a1\u00a7\u00bb\u00c1\u00d2\u00dd\u00e5"+
		"\u00e9\u00f0\u00f7\u00fc\u0102\u010a\u010d\u0113\u0119\u0120\u0124\u0136"+
		"\u013a\u0141\u014b\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}