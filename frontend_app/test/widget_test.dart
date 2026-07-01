import 'package:flutter_test/flutter_test.dart';
import 'package:frontend_app/main.dart';

void main() {
  testWidgets('TaskQuest app starts', (WidgetTester tester) async {
    await tester.pumpWidget(const TaskQuestApp());

    expect(find.byType(TaskQuestApp), findsOneWidget);
  });
}
